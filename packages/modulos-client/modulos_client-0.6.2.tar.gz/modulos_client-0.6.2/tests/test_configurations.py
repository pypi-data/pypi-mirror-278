from unittest import mock

from click.testing import CliRunner

from modulos_client.configurations import config_organizations


@mock.patch("modulos_client.config.ModulosClient.from_conf_file")
def test_get_organization_configurations(mock_client):
    # Prepare.
    org_response = mock.MagicMock()
    org_response.json.return_value = {"organization": {"id": "my_org_id"}}
    response = mock.MagicMock()
    response.ok = True
    response.json.return_value = {
        "organization_id": "my_org_id",
        "general": {"currency": "EUR"},
        "plan_quota": {"projects": 3},
    }
    mock_client.return_value.get.side_effect = [org_response, response]
    runner = CliRunner()

    # Test.
    result = runner.invoke(config_organizations, ["get"])

    # Check.
    assert result.exit_code == 0
    assert result.output == (
        "Key              Value\n"
        "---------------  -------------------\n"
        "organization_id  my_org_id\n"
        "general          {'currency': 'EUR'}\n"
        "plan_quota       {'projects': 3}\n"
    )


@mock.patch("modulos_client.config.ModulosClient.from_conf_file")
def test_update_organization_configurations(mock_client):
    # Prepare.
    response = mock.MagicMock()
    response.ok = True
    response.json.return_value = {
        "organization_id": "my_org_id",
        "general": {"currency": "EUR"},
        "plan_quota": {"projects": 4},
    }
    mock_client.return_value.patch.return_value = response
    runner = CliRunner()

    # Test.
    result = runner.invoke(
        config_organizations, ["update", "-o", "my_org_id", "--quota-projects", 4]
    )

    # Check.
    assert result.exit_code == 0
    assert result.output == (
        "Key              Value\n"
        "---------------  -------------------\n"
        "organization_id  my_org_id\n"
        "general          {'currency': 'EUR'}\n"
        "plan_quota       {'projects': 4}\n"
    )
