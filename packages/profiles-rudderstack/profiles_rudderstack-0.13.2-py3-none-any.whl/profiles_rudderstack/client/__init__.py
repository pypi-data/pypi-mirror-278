from typing import Union
import importlib
from google.protobuf import json_format
from profiles_rudderstack.go_client import get_gorpc
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel
from profiles_rudderstack.logger import Logger

from profiles_rudderstack.client.client_base import BaseClient
from profiles_rudderstack.client.snowpark import SnowparkClient
from profiles_rudderstack.client.warehouse import WarehouseClient


def WhClient(project_id: int, material_ref: int) -> BaseClient:
    """Returns a warehouse client based on the type of warehouse configured in siteconfig

    Returns:
        IClient: Warehouse client object
    """
    gorpc = get_gorpc()
    logger = Logger("WhtWarehouseClient")
    creds_response: tunnel.GetWarehouseCredentialsResponse = gorpc.GetWarehouseCredentials(
        tunnel.GetWarehouseCredentialsRequest(project_id=project_id, material_ref=material_ref))

    creds = json_format.MessageToDict(creds_response.credentials)
    schema = creds["schema"]
    wh_type = creds["type"]
    snowpark_enabled = False

    if wh_type == "snowflake":
        try:
            importlib.import_module('snowflake.snowpark.session')
            snowpark_enabled = True
        except ImportError:
            logger.warn(
                "snowpark not installed, using warehouse connector instead")

    if snowpark_enabled:
        return SnowparkClient(project_id, material_ref, creds, wh_type, schema)

    return WarehouseClient(project_id, material_ref, creds, wh_type, schema)
