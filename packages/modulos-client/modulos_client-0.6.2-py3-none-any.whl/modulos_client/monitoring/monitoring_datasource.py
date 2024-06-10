import requests

from modulos_client import config as config_utils


def monitoring_datasource_push(
    source_id: str,
    attribute_id: str,
    value: str | int | float,
    project_id: str,
):
    client = config_utils.ModulosClient.from_conf_file()
    try:
        response = client.post(
            f"/v1/projects/{project_id}/testing/logs",
            data={
                "source_id": source_id,
                "attribute_id": attribute_id,
                "value": value,
            },
        )
    except requests.exceptions.ConnectionError:
        print("Datasource push failed. Could not connect to the platform.")
        return None
    if response.status_code == 401:
        print(
            "Datasource push failed. There was an issue with the authorization. "
            "Please login again."
        )

        return None
    if response.ok:
        print("Datasource successfully submitted.")
        return None
    else:
        print(f"Datasource push failed: {response.text}")
        return None
