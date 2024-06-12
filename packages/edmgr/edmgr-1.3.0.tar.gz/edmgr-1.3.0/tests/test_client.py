from unittest.mock import Mock

from msal import TokenCache
import jwt
import pytest
from requests import HTTPError

from edmgr.config import settings
from edmgr.client import Client, _handle_response
from edmgr.exceptions import EdmAuthError, EdmTokenExpired, EdmAPIError, EdmEulaError
from .utils import get_jwt, make_response


@pytest.fixture
def valid_token_from_msal(monkeypatch):
    token = get_jwt(expires_in={"hours": 1})
    mock_func = Mock(return_value=token)
    monkeypatch.setattr("edmgr.client.msal_login", mock_func)


@pytest.fixture
def invalid_token_from_msal(monkeypatch):
    token = get_jwt(expires_in={"hours": -1})
    mock_func = Mock(return_value=token)
    monkeypatch.setattr("edmgr.client.msal_login", mock_func)


def test_handle_response_success():
    data = {"valid": "data"}
    response = make_response(data)
    handled_response = _handle_response(response)
    assert handled_response == data


def test_handle_response_invalid_code():
    data = {"valid": "data"}
    response = make_response(data, 500)
    with pytest.raises(HTTPError):
        _handle_response(response)


def test_handle_response_invalid_code_with_error():
    data = {"errorName": "Test Error"}
    response = make_response(data, 500)
    handled_response = _handle_response(response)
    assert handled_response == data


def test_handle_response_invalid_code_and_body():
    data = "Invalid JSON"
    response = make_response(data, 500)
    with pytest.raises(EdmAPIError):
        _handle_response(response)


def test_handle_response_valid_code_invalid_body():
    data = "Invalid JSON"
    response = make_response(data, 200)
    with pytest.raises(EdmAPIError):
        _handle_response(response)


def test_handle_response_404_code():
    data = {"errorCode": 404, "errorDescription": "Not Found"}
    response = make_response(data, 404)
    handled_response = _handle_response(response)
    assert handled_response == {}


def test_client_init_no_msal_token(test_settings_no_token, valid_token_from_msal):
    try:
        Client(msal_cache=TokenCache())
    except Exception as e:
        assert False, f"Caught exception: {e}"


def test_client_init_invalid_token(test_settings_invalid_token):
    with pytest.raises(EdmAuthError):
        Client(check_jwt_signature=False)


def test_client_init_invalid_msal_token(invalid_token_from_msal):
    with pytest.raises(EdmTokenExpired):
        Client(msal_cache=TokenCache())


def test_client_init_no_token(test_settings_no_token):
    client = Client()
    assert client.token is None


def test_client_assign_token(test_settings_no_token):
    client = Client(check_jwt_signature=False)
    token = get_jwt(expires_in={"hours": 2})
    client.token = token
    assert client.token == token


def test_client_assign_invalid_token(test_settings_no_token):
    client = Client(check_jwt_signature=False)
    token = get_jwt(expires_in={"hours": -1})
    with pytest.raises(EdmTokenExpired):
        client.token = token


def test_set_token(test_settings):
    settings_token = settings["access_token"]
    client = Client(check_jwt_signature=False)
    assert client.token == settings_token
    token = get_jwt(expires_in={"hours": 2})
    assert settings_token != token
    client._set_token(token, check_signature=False)
    assert client.token == token


def test_set_token_expired(test_settings):
    settings_token = settings["access_token"]
    client = Client(check_jwt_signature=False)
    assert client.token == settings_token
    token = get_jwt(expires_in={"hours": -1})
    assert settings_token != token
    with pytest.raises(EdmTokenExpired):
        client._set_token(token, check_signature=False)


def test_client_init_with_valid_token(test_settings_no_token):
    token = get_jwt(expires_in={"hours": 2})
    try:
        Client(token=token, check_jwt_signature=False)
    except Exception as e:
        assert False, f"Caught exception: {e}"


def test_client_init_msal(test_settings_no_token, valid_token_from_msal):
    try:
        Client(username="testuser", password="testpassword")
    except Exception as e:
        assert False, f"Caught exception: {e}"


def test_client_init_with_invalid_token(test_settings_no_token):
    token = get_jwt(expires_in={"hours": -1})
    with pytest.raises(EdmTokenExpired):
        Client(token=token, check_jwt_signature=False)


def test_client_init_valid_token(test_settings):
    client = Client(check_jwt_signature=False)
    assert client.token == settings["access_token"]
    try:
        jwt.decode(client.token, options={"verify_signature": False})
    except jwt.DecodeError as e:
        assert False, f"Invalid token: {e}"


def test_get_entitlements(test_settings, api_mock):
    api_data = api_mock["entitlements"]
    client = Client(check_jwt_signature=False)
    assert client.get_entitlements() == api_data["items"]


def test_get_entitlements_paginated(test_settings, api_mock):
    api_data = api_mock["entitlements"]
    client = Client(check_jwt_signature=False)
    params = {"offset": api_mock["offset"], "limit": api_mock["limit"]}
    assert params["limit"] == 1
    assert params["offset"] == 2
    assert client.get_entitlements(params=params) == [api_data["items"][1]]


def test_get_entitlements_empty(test_settings, api_mock_empty):
    client = Client(check_jwt_signature=False)
    assert client.get_entitlements() == []


def test_get_entitlement(test_settings, api_mock):
    api_data = api_mock["entitlements"]
    entitlement_id = api_mock["entitlement_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_entitlements(entitlement_id)[0] == api_data["items"][0]


def test_get_entitlement_raises(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_entitlements(entitlement_id)


def test_get_entitlement_404(test_settings, api_mock_empty_404):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_entitlements(entitlement_id) == []


def test_find_entitlements(test_settings, api_mock):
    api_data = api_mock["entitlements_by_product"]
    product_code = api_mock["product_code"]
    client = Client(check_jwt_signature=False)
    query = {"product.id": product_code}
    assert client.find_entitlements(query) == api_data["items"]


def test_get_releases(test_settings, api_mock):
    api_data = api_mock["releases"]
    entitlement_id = api_mock["entitlement_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_releases(entitlement_id) == api_data["items"]


@pytest.mark.parametrize("api_mock_empty", [404, 400, 500, 600], indirect=True)
def test_get_releases_empty(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_releases(entitlement_id) == []


def test_get_release(test_settings, api_mock):
    api_data = api_mock["releases"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    client = Client(check_jwt_signature=False)
    res = client.get_releases(entitlement_id, release_id)[0]
    assert res == api_data["items"][0]


def test_get_release_empty(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_releases(entitlement_id, release_id)


def test_get_artifacts(test_settings, api_mock):
    api_data = api_mock["releases"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    client = Client(check_jwt_signature=False)
    assert (
        client.get_artifacts(entitlement_id, release_id)
        == api_data["items"][0]["artifacts"]
    )


def test_get_artifacts_raises(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_artifacts(entitlement_id, release_id)


def test_get_artifacts_404(test_settings, api_mock_empty_404):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    release_id = api_mock_empty_404["release_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_artifacts(entitlement_id, release_id) == []


def test_get_artifact(test_settings, api_mock):
    api_data = api_mock["releases"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    artifact_id = api_mock["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client.get_artifacts(entitlement_id, release_id, artifact_id)[0]
    assert res == api_data["items"][0]["artifacts"][0]


def test_get_artifact_raises(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    artifact_id = api_mock_empty["artifact_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_artifacts(entitlement_id, release_id, artifact_id)


def test_get_artifact_404(test_settings, api_mock_empty_404):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    release_id = api_mock_empty_404["release_id"]
    artifact_id = api_mock_empty_404["artifact_id"]
    client = Client(check_jwt_signature=False)
    assert client.get_artifacts(entitlement_id, release_id, artifact_id) == []


@pytest.mark.parametrize("api_mock_empty", [404, 400, 500, 600], indirect=True)
def test_get_artifact_download_url_error(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    artifact_id = api_mock_empty["artifact_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_artifact_download_url(entitlement_id, release_id, artifact_id)


def test_get_artifact_download_url_eula_error(test_settings, api_mock_eula_error):
    api_data = api_mock_eula_error["eula_error"]
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client.get_artifact_download_url(entitlement_id, release_id, artifact_id)
    assert res == api_data


@pytest.mark.parametrize("api_mock_empty", [404, 400, 500, 600], indirect=True)
def test_get_artifact_fasp_spec_error(test_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    artifact_id = api_mock_empty["artifact_id"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmAPIError):
        client.get_artifact_download_url(entitlement_id, release_id, artifact_id)


def test_get_artifact_fasp_spec_eula_error(test_settings, api_mock_eula_error):
    api_data = api_mock_eula_error["eula_error"]
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client.get_artifact_fasp_spec(entitlement_id, release_id, artifact_id)
    assert res == api_data


def test_get_artifact_fasp_spec(test_settings, api_mock):
    api_data = api_mock["fasp_spec"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    artifact_id = api_mock["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client.get_artifact_fasp_spec(entitlement_id, release_id, artifact_id)
    assert res == api_data


def test_get_artifact_download_fasp(test_settings, api_mock):
    api_data = api_mock["fasp_spec"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    artifact_id = api_mock["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client._get_artifact_download_fasp(entitlement_id, release_id, artifact_id)
    assert res.error == {}
    assert res.spec == api_data["data"]["transfer_specs"][0]["transfer_spec"]


def test_get_artifact_download_fasp_eula_error(test_settings, api_mock_eula_error):
    eula_error = api_mock_eula_error["eula_error"]
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    client = Client(check_jwt_signature=False)
    res = client._get_artifact_download_fasp(entitlement_id, release_id, artifact_id)
    assert res.error["name"] == "eula-error"
    assert res.error["description"] == eula_error["errorDescription"]
    assert res.error["url"] == eula_error["agreementUrl"]


def test_get_artifact_download_http(test_settings, api_mock_with_download):
    entitlement_id = api_mock_with_download["entitlement_id"]
    release_id = api_mock_with_download["release_id"]
    artifact_id = api_mock_with_download["artifact_id"]
    file_data = api_mock_with_download["file_data"]
    client = Client(check_jwt_signature=False)
    download_stream = client.get_artifact_download_http(
        entitlement_id,
        release_id,
        artifact_id,
    )
    assert download_stream.error == {}
    assert download_stream.content_length == len(file_data)
    data = b""
    with download_stream as stream:
        for chunk in stream.iter_content():
            data += chunk
    assert data == file_data


def test_get_artifact_download_http_eula_error(test_settings, api_mock_eula_error):
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    eula_error = api_mock_eula_error["eula_error"]
    client = Client(check_jwt_signature=False)
    download_stream = client.get_artifact_download_http(
        entitlement_id,
        release_id,
        artifact_id,
    )
    assert download_stream.error["name"] == "eula-error"
    assert download_stream.error["description"] == eula_error["errorDescription"]
    assert download_stream.error["url"] == eula_error["agreementUrl"]
    assert download_stream.content_length == 0
    for _ in download_stream.iter_content():
        assert False, "Content is empty"


def test_download_artifact(test_settings, api_mock_with_download):
    entitlement_id = api_mock_with_download["entitlement_id"]
    release_id = api_mock_with_download["release_id"]
    artifact_id = api_mock_with_download["artifact_id"]
    mock_file = api_mock_with_download["mock_file"]
    file_data = api_mock_with_download["file_data"]
    file_name = api_mock_with_download["file_name"]
    client = Client(check_jwt_signature=False)
    with open(file_name, mode="wb") as file:
        bytes_written = client.download_artifact(
            file,
            entitlement_id,
            release_id,
            artifact_id,
        )
    assert bytes_written == len(file_data)
    try:
        mock_file.assert_called_once_with(file_name, mode="wb")
        mock_file().write.assert_called_once_with(file_data)
    except AssertionError as e:
        assert False, str(e)


def test_download_artifact_error(test_settings, api_mock_eula_error):
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    file_name = api_mock_eula_error["file_name"]
    eula_error = api_mock_eula_error["eula_error"]
    client = Client(check_jwt_signature=False)
    with pytest.raises(EdmEulaError) as excinfo:
        with open(file_name, mode="wb") as file:
            client.download_artifact(
                file,
                entitlement_id,
                release_id,
                artifact_id,
            )
    assert excinfo.value.description == eula_error["errorDescription"]
    assert excinfo.value.eula_url == eula_error["agreementUrl"]


def test_logout_token(test_settings):
    settings_token = settings["access_token"]
    client = Client(check_jwt_signature=False)
    assert client.token == settings_token
    client.logout()
    assert client.token is None
