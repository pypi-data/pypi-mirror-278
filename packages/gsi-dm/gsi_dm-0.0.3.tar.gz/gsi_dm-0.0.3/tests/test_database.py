from unittest.mock import patch

import pytest

from gsi.database import PostgresDB


def test_postgresdb_init():
    """Test the PostgresDB class initialization."""
    # Test that the class raises a TypeError if the required arguments are not provided
    with pytest.raises(TypeError):
        PostgresDB()

    with patch("getpass.getpass", return_value="test") as mock_getpass:
        db = PostgresDB(host="localhost", database="test", user="test")
        mock_getpass.assert_called_once_with(
            "The script database.py wants the password for PostgresDB(host=localhost, database=test, user=test): ",
        )
        assert db.passwd == "test"  # noqa

    db = PostgresDB(
        host="localhost",
        database="mydb",
        user="testuser",
        passwd="testpass",  # noqa
    )
    assert isinstance(db, PostgresDB)
    assert db.host == "localhost"
    assert db.port == 5432
    assert db.database == "mydb"
    assert db.user == "testuser"
    assert db.passwd == "testpass"  # noqa
    assert db.conn is None
    assert db.in_transaction is False


def test_postgresdb_repr():
    """Test the PostgresDB class __repr__ method."""
    db = PostgresDB(
        host="localhost",
        database="mydb",
        user="testuser",
        passwd="testpass",  # noqa
    )
    assert repr(db) == "PostgresDB(host=localhost, database=mydb, user=testuser)"
