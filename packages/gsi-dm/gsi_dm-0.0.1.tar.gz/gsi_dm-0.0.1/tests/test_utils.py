import pytest
from pathlib import Path

from gsi.utils import detect_file_encoding, ColorGradient


def test_detect_file_encoding():
    """Test the detect_file_encoding function"""
    # Assert that a nonexistint file raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        detect_file_encoding(Path("nonexistent_file.txt"))
    # Test that the function returns a tuple of text, encoding, and confidence
    assert isinstance(detect_file_encoding(Path("tests/test_utils.py")), tuple)
    # Test that the function returns the expected values for a known file
    text, encoding, confidence = detect_file_encoding(Path("tests/test_utils.py"))
    assert isinstance(text, str)
    assert isinstance(encoding, str)
    assert isinstance(confidence, float)
    assert confidence >= 0.0 and confidence <= 1.0
    assert "import pytest" in text and "test_detect_file_encoding" in text


def test_color_gradient_init():
    """Test that the ColorGradient class initializes."""
    cg = ColorGradient("#000000", "#FFFFFF", 10)
    assert isinstance(cg, ColorGradient)
    assert cg.start_hex == "#000000"
    assert cg.finish_hex == "#FFFFFF"
    assert cg.n == 10


def test_color_gradient_color_dict():
    """Test that the ColorGradient class color_dict method returns the expected values."""
    cg = ColorGradient("#000000", "#FFFFFF", 10)
    gradient = cg.color_dict([[0, 0, 0], [255, 255, 255]])
    assert isinstance(gradient, dict)
    assert "hex" in gradient
    assert "rgb" in gradient
    assert "r" in gradient
    assert "g" in gradient
    assert "b" in gradient
    assert gradient["hex"] == ["#000000", "#ffffff"]
    assert gradient["rgb"] == [[0, 0, 0], [255, 255, 255]]
    assert gradient["r"] == [0, 255]
    assert gradient["g"] == [0, 255]
    assert gradient["b"] == [0, 255]


def test_color_gradient_linear_gradient():
    """Test the linear_gradient method of the ColorGradient class."""
    cg = ColorGradient("#000000", "#FFFFFF", 4)
    gradient = cg.linear_gradient()
    assert isinstance(gradient, dict)
    assert (
        len(gradient["hex"]) == 4
        and len(gradient["rgb"]) == 4
        and len(gradient["r"]) == 4
        and len(gradient["g"]) == 4
        and len(gradient["b"]) == 4
    )
    assert gradient["hex"] == ["#000000", "#555555", "#aaaaaa", "#ffffff"]
    assert gradient["rgb"] == [
        [0, 0, 0],
        [85, 85, 85],
        [170, 170, 170],
        [255, 255, 255],
    ]
    assert (
        gradient["r"] == [0, 85, 170, 255]
        and gradient["g"] == [0, 85, 170, 255]
        and gradient["b"] == [0, 85, 170, 255]
    )


def test_color_gradient_hex_to_rgb():
    """Test the class method hex_to_rgb of the ColorGradient class."""
    assert ColorGradient.hex_to_rgb("#000000") == [0, 0, 0]
    assert ColorGradient.hex_to_rgb("#FFFFFF") == [255, 255, 255]
    assert ColorGradient.hex_to_rgb("#00FF00") == [0, 255, 0]
    assert ColorGradient.hex_to_rgb("#FF00FF") == [255, 0, 255]
    assert ColorGradient.hex_to_rgb("#0000FF") == [0, 0, 255]
    assert ColorGradient.hex_to_rgb("#FF0000") == [255, 0, 0]


def test_color_gradient_rgb_to_hex():
    """Test the class method rgb_to_hex of the ColorGradient class."""
    assert ColorGradient.rgb_to_hex([0, 0, 0]) == "#000000"
    assert ColorGradient.rgb_to_hex([255, 255, 255]) == "#ffffff"
    assert ColorGradient.rgb_to_hex([0, 255, 0]) == "#00ff00"
    assert ColorGradient.rgb_to_hex([255, 0, 255]) == "#ff00ff"
    assert ColorGradient.rgb_to_hex([0, 0, 255]) == "#0000ff"
    assert ColorGradient.rgb_to_hex([255, 0, 0]) == "#ff0000"
