import pytest
from requests.exceptions import RequestException
from requests_mock import NoMockAddress

from edmgr.requester import Requester


def test_requester_get_simple(requests_mock):
    requests_mock.get("https://test.api.com", json={"data": "my_data"})
    requester = Requester()
    resp = requester.get("https://test.api.com")
    assert resp.status_code == 200
    assert resp.json()["data"] == "my_data"


def test_requester_get_with_base_url(requests_mock):
    base_url = "https://test.api.com"
    requests_mock.get(base_url, json={"data": "base_url_data"})
    requester = Requester(base_url)
    assert requester.base_url == base_url
    resp = requester.get()
    assert resp.status_code == 200
    assert resp.json()["data"] == "base_url_data"


def test_requester_get_with_endpoint(requests_mock):
    base_url = "https://test.api.com"
    endpoint = "api/v1/my-endpoint"
    requests_mock.get(f"{base_url}/{endpoint}", json={"data": "endpoint_data"})
    requester = Requester(base_url)
    resp = requester.get(endpoint)
    assert resp.status_code == 200
    assert resp.json()["data"] == "endpoint_data"


def test_requester_get_with_path(requests_mock):
    base_url = "https://test.api.com"
    endpoint = "api/v1/my-endpoint"
    path = "resource/12345"
    requests_mock.get(f"{base_url}/{endpoint}/{path}", json={"data": "path_data"})
    requester = Requester(f"{base_url}/{endpoint}")
    resp = requester.get(path)
    assert resp.status_code == 200
    assert resp.json()["data"] == "path_data"


def test_requester_get_none(caplog):
    requester = Requester()
    resp = requester.get()
    assert resp is None
    resp = requester.get("not_a_url")
    assert resp is None
    assert len(caplog.records) == 2
    for log_record in caplog.records:
        assert log_record.levelname == "ERROR"
        assert log_record.msg.startswith("Invalid URL")


def test_requester_get_raises():
    requester = Requester(raise_request_exc=True)
    with pytest.raises(RequestException):
        requester.get()


def test_requester_get_token_required(requests_mock):
    token = "T0k3n"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"data": "my_data"}
    requests_mock.get("https://test.api.com", request_headers=headers, json=data)
    requester = Requester()
    with pytest.raises(NoMockAddress):
        requester.get("https://test.api.com")


def test_requester_get_with_token(requests_mock):
    token = "T0k3n"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"data": "my_data"}
    requests_mock.get("https://test.api.com", request_headers=headers, json=data)
    requester = Requester(token=token)
    assert requester.token == token
    resp = requester.get("https://test.api.com")
    assert resp.status_code == 200
    assert resp.json()["data"] == "my_data"


def test_requester_set_token(requests_mock):
    token = "T0k3n"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"data": "my_data"}
    requests_mock.get("https://test.api.com", request_headers=headers, json=data)
    requester = Requester()
    requester.token = token
    assert requester.token == token
    resp = requester.get("https://test.api.com")
    assert resp.status_code == 200
    assert resp.json()["data"] == "my_data"
