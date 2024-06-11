from pandas import DataFrame
from typing import Any, Optional, Union, Iterator
from abc import ABC, abstractmethod
from profiles_rudderstack.go_client import get_gorpc
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel
from profiles_rudderstack.wh.connector_base import ConnectorBase


# Base Interfcae for client
class BaseClient(ABC):
    def __init__(self, project_id: int, material_ref: int, schema: str) -> None:
        self.__gorpc = get_gorpc()
        self.__project_id = project_id
        self.__material_ref = material_ref
        self.snowpark_session: Any = None
        self.is_snowpark_enabled: bool = False
        self.wh_connection: Optional[ConnectorBase] = None
        self.schema = schema

    def query_sql_without_result(self, sql: str):
        self.__gorpc.QuerySqlWithoutResult(
            tunnel.QuerySqlWithoutResultRequest(project_id=self.__project_id, material_ref=self.__material_ref, sql=sql))

    def query_template_without_result(self, template: str):
        self.__gorpc.QueryTemplateWithoutResult(tunnel.QueryTemplateWithoutResultRequest(
            project_id=self.__project_id, material_ref=self.__material_ref, template=template))

    @abstractmethod
    def query_sql_with_result(self, sql: str) -> DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def get_df(self, selector_sql: str, batching: bool, batch_size: int) -> Union[DataFrame, Iterator[DataFrame]]:
        raise NotImplementedError()

    def get_snowpark_df(self, selector_sql: str):
        raise NotImplementedError(
            "get_snowpark_df is only supported for Snowpark enabled Snowflake warehouse, please use get_df for non-Snowpark enabled warehouses")

    @abstractmethod
    def write_df_to_table(self, df, table: str, schema: str = "", append_if_exists: bool = False) -> None:
        raise NotImplementedError()
