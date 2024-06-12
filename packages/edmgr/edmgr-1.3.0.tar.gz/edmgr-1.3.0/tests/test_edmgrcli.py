import json
import logging
from pathlib import Path
from unittest.mock import MagicMock

from click.testing import CliRunner
import pytest

from edmgr.config import settings
from edmgr.client import Client
from edmgr import edmgrcli


@pytest.fixture
def cached_token_from_settings(monkeypatch):
    token = settings["access_token"]
    mock_cached_client = MagicMock()
    mock_cached_client.return_value.__enter__.return_value = Client(
        token=token, check_jwt_signature=False
    )
    monkeypatch.setattr("edmgr.edmgrcli.cached_client", mock_cached_client)
    mock_get_current_token = MagicMock()
    mock_get_current_token.return_value = token
    monkeypatch.setattr("edmgr.edmgrcli.get_current_token", mock_get_current_token)
    return token


def test_default_verbosity():
    runner = CliRunner()
    result = runner.invoke(edmgrcli.cli)
    assert result.exit_code == 0
    assert settings["log_level"] == logging.ERROR


def test_show_token(test_settings, cached_token_from_settings):
    token = cached_token_from_settings
    runner = CliRunner()
    result = runner.invoke(edmgrcli.show_token)
    assert result.exit_code == 0
    assert f"- Access Token: {token}" in result.output


def test_show_token_error(test_settings_invalid_token):
    runner = CliRunner()
    result = runner.invoke(edmgrcli.show_token)
    assert result.exit_code == 1


def test_entitlements_json(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements"]["items"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-f", "json"])
    assert result.exit_code == 0
    assert json.loads(result.output) == items


def test_entitlements_paginated_json(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["entitlements"]["items"]
    limit = api_mock["limit"]
    offset = api_mock["offset"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlements, ["-l", limit, "-o", offset, "-f", "json"]
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == [items[1]]


def test_entitlements(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements"]["items"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements)
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert items[1]["id"] in result.output
    assert items[1]["product"]["id"] in result.output


def test_entitlements_by_product(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements_by_product"]["items"]
    product_code = api_mock["product_code"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-p", product_code])
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output


def test_entitlements_by_product_and_filter_out_id(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["entitlements_by_product"]["items"]
    product_code = api_mock["product_code"]
    entitlement_id = "0000"
    assert entitlement_id not in list(map(lambda x: x["id"], items))
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlements, ["-p", product_code, "-e", entitlement_id]
    )
    assert result.exit_code == 0
    assert items[0]["id"] not in result.output
    assert items[0]["product"]["id"] not in result.output
    assert "Couldn't find Entitlements" in result.output


def test_entitlements_paginated(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements"]["items"]
    limit = api_mock["limit"]
    offset = api_mock["offset"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-l", limit, "-o", offset])
    assert result.exit_code == 0
    assert items[0]["id"] not in result.output
    assert items[0]["product"]["id"] not in result.output
    assert items[1]["id"] in result.output
    assert items[1]["product"]["id"] in result.output


def test_entitlements_not_found(
    test_settings, cached_token_from_settings, api_mock_empty
):
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements)
    assert result.exit_code == 0
    assert "Couldn't find any Entitlements" in result.output


def test_entitlement_filter(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements"]["items"]
    entitlement_id = api_mock["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-e", entitlement_id])
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert items[1]["id"] not in result.output
    assert items[1]["product"]["id"] not in result.output


def test_entitlement(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["entitlements"]["items"]
    entitlement_id = api_mock["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlement, [entitlement_id])
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert items[1]["id"] not in result.output
    assert items[1]["product"]["id"] not in result.output


def test_virtual_entitlement(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["virtual_entitlements"]["items"]
    grouped_entitlements = items[0]["virtualEntitlements"]
    virtual_entitlements_id = api_mock["virtual_entitlements_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlement, [virtual_entitlements_id])
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert grouped_entitlements[0]["id"] in result.output
    assert grouped_entitlements[1]["id"] in result.output
    assert grouped_entitlements[2]["id"] in result.output
    assert "Showing from 1 to 3 of 3" in result.output


def test_virtual_entitlement_paging(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["virtual_entitlements"]["items"]
    grouped_entitlements = items[0]["virtualEntitlements"]
    virtual_entitlements_id = api_mock["virtual_entitlements_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlement, [virtual_entitlements_id, "-o", 2, "-l", 1]
    )
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert grouped_entitlements[0]["id"] not in result.output
    assert grouped_entitlements[1]["id"] in result.output
    assert grouped_entitlements[2]["id"] not in result.output
    assert "Showing from 2 to 2 of 3" in result.output


def test_virtual_entitlement_out_of_range(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["virtual_entitlements"]["items"]
    virtual_entitlements_id = api_mock["virtual_entitlements_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlement, [virtual_entitlements_id, "-o", 4, "-l", 1]
    )
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert "Entitlements page out of range." in result.output


def test_virtual_entitlement_filter_by_product(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["virtual_entitlements"]["items"]
    grouped_entitlements = items[0]["virtualEntitlements"]
    virtual_entitlements_id = api_mock["virtual_entitlements_id"]
    product_code = api_mock["virtual_entitlement_product_code"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlement, [virtual_entitlements_id, "-p", product_code]
    )
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert grouped_entitlements[0]["id"] not in result.output
    assert grouped_entitlements[1]["id"] in result.output
    assert grouped_entitlements[2]["id"] not in result.output


def test_virtual_entitlement_filter_by_product_empty(
    test_settings, cached_token_from_settings, api_mock
):
    items = api_mock["virtual_entitlements"]["items"]
    grouped_entitlements = items[0]["virtualEntitlements"]
    virtual_entitlements_id = api_mock["virtual_entitlements_id"]
    product_code = "00000"
    assert product_code not in list(
        map(lambda x: x["product"]["id"], grouped_entitlements)
    )
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.entitlement, [virtual_entitlements_id, "-p", product_code]
    )
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["product"]["id"] in result.output
    assert grouped_entitlements[0]["id"] not in result.output
    assert grouped_entitlements[1]["id"] not in result.output
    assert grouped_entitlements[2]["id"] not in result.output
    assert "No Entitlement were found" in result.output


def test_entitlement_raises(test_settings, cached_token_from_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-e", entitlement_id])
    assert result.exit_code == 1


def test_entitlement_not_found(
    test_settings, cached_token_from_settings, api_mock_empty_404
):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.entitlements, ["-e", entitlement_id])
    assert result.exit_code == 0
    assert "Couldn't find Entitlement" in result.output


def test_releases_json(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"]
    entitlement_id = api_mock["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id, "-f", "json"])
    assert result.exit_code == 0
    assert json.loads(result.output) == items


def test_releases(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"]
    entitlement_id = api_mock["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id])
    assert result.exit_code == 0
    assert items[0]["entitlement"]["id"] in result.output
    assert items[0]["id"] in result.output
    assert items[1]["id"] in result.output


def test_releases_not_found(test_settings, cached_token_from_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id])
    assert result.exit_code == 0
    assert "Couldn't find any Release" in result.output


def test_release(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 0
    assert items[0]["entitlement"]["id"] in result.output
    assert items[0]["id"] in result.output
    assert items[1]["id"] not in result.output


def test_release_raises(test_settings, cached_token_from_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 1


def test_release_not_found(
    test_settings, cached_token_from_settings, api_mock_empty_404
):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    release_id = api_mock_empty_404["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.releases, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 0
    assert (
        "Couldn't find Release with the given Entitlement ID & Release ID"
        in result.output
    )


def test_artifacts_json(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"][0]["artifacts"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id, "-f", "json"]
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == items


def test_artifacts(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"][0]["artifacts"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["name"] in result.output
    assert items[1]["id"] in result.output
    assert items[1]["name"] in result.output


def test_artifacts_raises(test_settings, cached_token_from_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 1


def test_artifacts_not_found(
    test_settings, cached_token_from_settings, api_mock_empty_404
):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    release_id = api_mock_empty_404["release_id"]
    runner = CliRunner()
    result = runner.invoke(edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id])
    assert result.exit_code == 0
    assert (
        result.output
        == "Couldn't find artifacts with the given Entitlement & Release\n"
    )


def test_artifact(test_settings, cached_token_from_settings, api_mock):
    items = api_mock["releases"]["items"][0]["artifacts"]
    entitlement_id = api_mock["entitlement_id"]
    release_id = api_mock["release_id"]
    artifact_id = api_mock["artifact_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id, "-a", artifact_id]
    )
    assert result.exit_code == 0
    assert items[0]["id"] in result.output
    assert items[0]["name"] in result.output
    assert items[1]["id"] not in result.output
    assert items[1]["name"] not in result.output


def test_artifact_raises(test_settings, cached_token_from_settings, api_mock_empty):
    entitlement_id = api_mock_empty["entitlement_id"]
    release_id = api_mock_empty["release_id"]
    artifact_id = api_mock_empty["artifact_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id, "-a", artifact_id]
    )
    assert result.exit_code == 1


def test_artifact_not_found(
    test_settings, cached_token_from_settings, api_mock_empty_404
):
    entitlement_id = api_mock_empty_404["entitlement_id"]
    release_id = api_mock_empty_404["release_id"]
    artifact_id = api_mock_empty_404["artifact_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.artifacts, ["-e", entitlement_id, "-r", release_id, "-a", artifact_id]
    )
    assert result.exit_code == 0
    assert (
        result.output
        == "Couldn't find artifacts with the given Entitlement, Release & Artifact\n"
    )


def test_download_artifacts_single(
    test_settings, cached_token_from_settings, api_mock_with_download
):
    entitlement_id = api_mock_with_download["entitlement_id"]
    release_id = api_mock_with_download["release_id"]
    artifact_id = api_mock_with_download["artifact_id"]
    mock_file = api_mock_with_download["mock_file"]
    file_data = api_mock_with_download["file_data"]
    file_name = api_mock_with_download["file_name"]
    file_path = (Path(settings["downloads"]) / file_name).expanduser().resolve()
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.download_artifacts,
        ["-e", entitlement_id, "-r", release_id, "-a", artifact_id],
    )
    assert result.exit_code == 0
    assert f"Downloading {file_path}" in result.output
    try:
        mock_file.assert_called_once_with(file_path, mode="wb")
        mock_file().write.assert_called_once_with(file_data)
    except AssertionError as e:
        assert False, str(e)


def test_download_controlled_artifacts_single(
    test_settings, cached_token_from_settings, api_mock_with_download_controlled
):
    mock_file = api_mock_with_download_controlled["mock_file"]
    file_data = api_mock_with_download_controlled["file_data"]
    file_name = api_mock_with_download_controlled["file_name"]
    file_path = (Path(settings["downloads"]) / file_name).expanduser().resolve()
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.download_artifacts,
        [
            "-e",
            api_mock_with_download_controlled["entitlement_id"],
            "-r",
            api_mock_with_download_controlled["release_id"],
            "-a",
            api_mock_with_download_controlled["artifact_id"],
        ],
    )
    assert result.exit_code == 0
    assert "Controlled IP found. Starting download via http..." in result.output
    assert f"Downloading {file_path}" in result.output
    try:
        mock_file.assert_called_once_with(file_path, mode="wb")
        mock_file().write.assert_called_once_with(file_data)
    except AssertionError as e:
        assert False, str(e)


def test_download_artifacts_eula_error_abort(
    test_settings, cached_token_from_settings, api_mock_eula_error
):
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.download_artifacts,
        ["-e", entitlement_id, "-r", release_id, "-a", artifact_id],
        input="n\nn\n",
    )
    assert result.exit_code == 1


def test_download_artifacts_eula_error(
    test_settings, cached_token_from_settings, api_mock_eula_error
):
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    eula_error_message = api_mock_eula_error["eula_error"]["errorDescription"]
    mock_file = api_mock_eula_error["mock_file"]
    file_data = api_mock_eula_error["file_data"]
    file_name = api_mock_eula_error["file_name"]
    file_path = (Path(settings["downloads"]) / file_name).expanduser().resolve()

    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.download_artifacts,
        ["-e", entitlement_id, "-r", release_id, "-a", artifact_id],
        input="n\ny\n",
    )
    assert result.exit_code == 0
    assert eula_error_message in result.output
    assert f"Downloading {file_path}" in result.output
    try:
        mock_file.assert_called_once_with(file_path, mode="wb")
        mock_file().write.assert_called_once_with(file_data)
    except AssertionError as e:
        assert False, str(e)


def test_download_artifacts_eula_error_open_browser(
    test_settings, cached_token_from_settings, api_mock_eula_error
):
    entitlement_id = api_mock_eula_error["entitlement_id"]
    release_id = api_mock_eula_error["release_id"]
    artifact_id = api_mock_eula_error["artifact_id"]
    eula_error_message = api_mock_eula_error["eula_error"]["errorDescription"]
    agreement_url = api_mock_eula_error["eula_error"]["agreementUrl"]
    mock_file = api_mock_eula_error["mock_file"]
    file_data = api_mock_eula_error["file_data"]
    file_name = api_mock_eula_error["file_name"]
    webbrowser_open = api_mock_eula_error["mock_webbrowser_open"]
    file_path = (Path(settings["downloads"]) / file_name).expanduser().resolve()

    runner = CliRunner()
    result = runner.invoke(
        edmgrcli.download_artifacts,
        ["-e", entitlement_id, "-r", release_id, "-a", artifact_id],
        input="y\ny\n",
    )
    # assert result.exit_code == 0
    assert eula_error_message in result.output
    assert f"Downloading {file_path}" in result.output
    try:
        mock_file.assert_called_once_with(file_path, mode="wb")
        mock_file().write.assert_called_once_with(file_data)
        webbrowser_open.assert_called_once_with(agreement_url)
    except AssertionError as e:
        assert False, str(e)
