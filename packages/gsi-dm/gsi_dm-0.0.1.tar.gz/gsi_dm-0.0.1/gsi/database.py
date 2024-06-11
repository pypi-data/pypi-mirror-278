#!/usr/bin/env python

from __future__ import annotations

import logging
from typing import Iterator
from pathlib import Path
import polars as pl
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.sql import Composable
import getpass

from gsi.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class PostgresDB:
    """Base database object."""

    def __init__(
        self: PostgresDB,
        host: str,
        database: str,
        user: str,
        **kwargs,
    ) -> None:
        self.host = host
        self.database = database
        self.user = user
        if ("passwd" in kwargs and kwargs["passwd"] is not None) or (
            "password" in kwargs and kwargs["password"] is not None
        ):
            self.passwd = kwargs["passwd"]
        else:
            self.passwd = self.get_password()
        self.port = 5432
        self.in_transaction = False
        self.encoding = "UTF8"
        self.conn = None

    def __repr__(self: PostgresDB) -> str:
        return f"{self.__class__.__name__}(host={self.host}, database={self.database}, user={self.user})"  # noqa: E501

    def __del__(self: PostgresDB) -> None:
        """Delete the instance."""
        self.close()

    def get_password(self):
        return getpass.getpass(
            f"The script {Path(__file__).name} wants the password for {self!s}: ",
        )

    def open_db(self: PostgresDB) -> None:
        """Open a database connection."""

        def db_conn(db):
            """Return a database connection object."""
            return psycopg2.connect(
                host=str(db.host),
                database=str(db.database),
                port=db.port,
                user=str(db.user),
                password=str(db.passwd),
            )

        if self.conn is None:
            self.conn = db_conn(self)
            self.conn.set_session(autocommit=False)
        self.encoding = self.conn.encoding

    def cursor(self: PostgresDB):
        """Return the connection cursor."""
        self.open_db()
        return self.conn.cursor(cursor_factory=DictCursor)

    def close(self: PostgresDB) -> None:
        """Close the database connection."""
        self.rollback()
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit(self: PostgresDB) -> None:
        """Commit the current transaction."""
        if self.conn:
            self.conn.commit()
        self.in_transaction = False

    def rollback(self: PostgresDB) -> None:
        """Roll back the current transaction."""
        if self.conn is not None:
            self.conn.rollback()
        self.in_transaction = False

    def execute(self: PostgresDB, sql: str | Composable, params=None):
        """A shortcut to self.cursor().execute() that handles encoding.

        Handles insert, updates, deletes
        """
        self.in_transaction = True
        try:
            curs = self.cursor()
            logger.debug(f"Executing SQL: {sql}")
            if isinstance(sql, Composable):
                curs.execute(sql)
            else:
                if params is None:
                    curs.execute(sql.encode(self.encoding))
                else:
                    curs.execute(sql.encode(self.encoding), params)
        except Exception:
            self.rollback()
            raise
        return curs

    def rowdict(self: PostgresDB, sql: str | Composable, params=None) -> tuple:
        """Convert a cursor object to an iterable that.

        yields dictionaries of row data.
        """
        curs = self.execute(sql, params)
        headers = [d[0] for d in curs.description]

        def dict_row():
            """Convert a data row to a dictionary."""
            row = curs.fetchone()
            if row:
                if self.encoding:
                    r = [
                        (
                            c.decode(self.encoding, "backslashreplace")
                            if isinstance(c, bytes)
                            else c
                        )
                        for c in row
                    ]
                else:
                    r = row
                return dict(zip(headers, r, strict=True))
            return None

        return (iter(dict_row, None), headers, curs.rowcount)

    def dataframe(
        self: PostgresDB,
        sql: str | Composable,
        params=None,
        **kwargs,
    ) -> pl.DataFrame:
        """Return query results as a Polars dataframe object."""
        try:
            data, cols, rowcount = self.rowdict(sql, params)
        except Exception as e:
            logger.exception(f"Error fetching data: {e}")
            return pl.DataFrame()
        data, cols, rowcount = self.rowdict(sql, params)
        return pl.DataFrame(data, infer_schema_length=rowcount, **kwargs)
