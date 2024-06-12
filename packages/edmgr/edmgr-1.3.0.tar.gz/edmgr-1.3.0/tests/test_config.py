import pytest

from edmgr.config import (
    PROD,
    QA,
    Settings,
    get_log_level,
    get_log_level_from_verbose,
    LOG_LEVELS,
)


def test_settings_class_default_env():
    settings = Settings()
    assert settings._env == PROD


def test_settings_getitem():
    settings = Settings()
    settings._env["test_item"] = "test_value"
    assert settings["test_item"] == "test_value"


def test_settings_getitem_raises():
    settings = Settings()
    with pytest.raises(KeyError):
        settings["not_present_item"]


def test_settings_setitem():
    settings = Settings()
    settings["test_item"] = "test_value"
    assert settings._env["test_item"] == "test_value"


def test_settings_get():
    settings = Settings()
    settings._env["test_item"] = "test_value"
    assert settings.get("test_item") == "test_value"
    assert settings.get("not_present_item") is None
    assert settings.get("not_present_item", "my_default_value") == "my_default_value"


def test_settings_set_env():
    settings = Settings()
    settings.set_env("qa")
    assert settings._env == QA


def test_settings_set_env_raises():
    settings = Settings()
    with pytest.raises(ValueError):
        settings.set_env("invalid_env")


def test_get_log_level():
    assert get_log_level("INFO") == LOG_LEVELS["info"]


def test_get_log_level_raises():
    with pytest.raises(ValueError):
        get_log_level("NOT_A_LOG_LEVEL")


def test_get_log_level_from_verbose():
    assert get_log_level_from_verbose(0) == LOG_LEVELS["error"]
    assert get_log_level_from_verbose(1) == LOG_LEVELS["warning"]
    assert get_log_level_from_verbose(2) == LOG_LEVELS["info"]
    assert get_log_level_from_verbose(3) == LOG_LEVELS["debug"]


def test_get_log_level_from_verbose_raises():
    with pytest.raises(ValueError):
        get_log_level_from_verbose(4)
