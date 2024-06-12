from pathlib import Path

from unittest.mock import mock_open, create_autospec

import jwt
import pytest

from edmgr.auth import (
    decode_jwt_token,
    delete_cache,
    _write_cache,
)
from edmgr.exceptions import EdmAuthError, EdmTokenExpired
from .utils import get_token_params, get_jwt


def test_decode_jwt_token():
    params = get_token_params(expires_in={"hours": 1})
    encoded_token = jwt.encode(params, "secret", algorithm="HS256")
    payload = decode_jwt_token(encoded_token, check_signature=False)
    assert payload == params


def test_decode_jwt_token_invalid():
    expired_token = get_jwt(expires_in={"hours": -1})
    with pytest.raises(EdmTokenExpired):
        decode_jwt_token(expired_token, check_signature=False)
    with pytest.raises(EdmAuthError):
        decode_jwt_token("not-a-jwt", check_signature=False)


def test_remove_cached_token(monkeypatch):
    mock_unlink = create_autospec(Path.unlink)
    monkeypatch.setattr(Path, "unlink", mock_unlink)
    mock_is_file = create_autospec(Path.is_file)
    mock_is_file.return_value = True
    monkeypatch.setattr(Path, "is_file", mock_is_file)
    delete_cache()
    assert len(mock_is_file.mock_calls) == 2
    assert len(mock_unlink.mock_calls) == 2


def test_write_cache(monkeypatch):
    data = {"test": "data"}
    cache_file = Path("test/path/cache")
    mock_mkdir = create_autospec(Path.mkdir)
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    mock_open_func = mock_open()
    monkeypatch.setattr("builtins.open", mock_open_func)
    _write_cache(data, cache_file)
    try:
        mock_mkdir.assert_called_once_with(
            Path("test/path"), mode=0o700, parents=True, exist_ok=True
        )
    except AssertionError as e:
        assert False, f"mkdir: {e}"
    try:
        mock_open_func.assert_called_once()
    except AssertionError as e:
        assert False, f"mkdir: {e}"
    mock_file = mock_open_func()
    try:
        mock_file.write.assert_called_once_with(data)
    except AssertionError as e:
        assert False, f"write: {e}"
