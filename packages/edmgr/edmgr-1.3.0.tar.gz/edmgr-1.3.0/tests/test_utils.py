import pytest

from edmgr.utils import convert_bytes_size


@pytest.mark.parametrize(
    "bytes_size,system,decimal_places,result",
    [
        (10_244, "metric", 3, "10.244 kB"),
        (1000 * 1000, "metric", 3, "1 MB"),
        (1_024_466, "metric", 3, "1.024 MB"),
        (8_435_689_870, "metric", 3, "8.436 GB"),
        (10_244, "binary", 3, "10.004 KiB"),
        (1024 * 1024, "binary", 3, "1 MiB"),
        (1_024_466, "binary", 3, "1000.455 KiB"),
        (8_435_689_870, "binary", 3, "7.856 GiB"),
    ],
)
def test_convert_bytes_size(bytes_size, system, decimal_places, result):
    assert convert_bytes_size(bytes_size, system, decimal_places) == result


def test_convert_bytes_size_raises():
    with pytest.raises(ValueError):
        convert_bytes_size(1, system="invalid_system")
