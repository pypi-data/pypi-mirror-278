import json
from os import path
from typing import Literal, Optional, List, Dict, Any, Union
from google.protobuf import json_format
import pandas as pd
from profiles_rudderstack.go_client import get_gorpc
from profiles_rudderstack.logger import Logger
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel
from profiles_rudderstack.client import SnowparkClient
from profiles_rudderstack.wht_context import WhtContextStore


class Contract:
    def __init__(self, contract_ref: int) -> None:
        self.__contract_ref = contract_ref

    def ref(self) -> int:
        return self.__contract_ref


class BaseWhtProject:
    def __init__(self, project_id: int, material_ref: int) -> None:
        self.__gorpc = get_gorpc()
        self.__material_ref = material_ref
        self.__project_id = project_id

    def project_path(self) -> str:
        """Get the project path

        Returns:
            str: project folder
        """
        project_path_res: tunnel.GetProjectPathResponse = self.__gorpc.GetProjectPath(
            tunnel.GetProjectPathRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return project_path_res.project_path

    def is_rudder_backend(self) -> bool:
        is_rudder_backend_res: tunnel.GetIsRudderBackendResponse = self.__gorpc.GetIsRudderBackend(
            tunnel.GetIsRudderBackendRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return is_rudder_backend_res.is_rudder_backend

    def entities(self) -> Dict[str, Any]:
        """Get the entities of the project

        Returns:
            Dict: Entities of the project
        """
        entities_res: tunnel.GetEntitiesResponse = self.__gorpc.GetEntities(
            tunnel.GetEntitiesRequest(project_id=self.__project_id, material_ref=self.__material_ref))
        entities = {}
        for key, entity in entities_res.entities.items():
            entities[key] = json_format.MessageToDict(entity)

        return entities


class WhtModel:
    def __init__(self, project_id: int, material_ref: int):
        self.__project_id = project_id
        self.__material_ref = material_ref
        self.__gorpc = get_gorpc()
        self.logger = Logger("WhtModel")

    def name(self) -> str:
        """Get the name of the model

        Returns:
            str: Name of the model
        """
        nameResponse: tunnel.ModelNameResponse = self.__gorpc.ModelName(
            tunnel.NameRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return nameResponse.model_name

    def db_object_name_prefix(self) -> str:
        """Get the db object name prefix of the model

        Returns:
            str: db object name prefix of the model
        """
        dbObjectNamePrefixResponse: tunnel.DbObjectNamePrefixResponse = self.__gorpc.DbObjectNamePrefix(
            tunnel.DbObjectNamePrefixRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return dbObjectNamePrefixResponse.db_object_name_prefix

    def materialization(self) -> dict:
        """Get the materialization of the model

        Returns:
            str: Materialization of the model
        """
        mznResponse: tunnel.MaterializationResponse = self.__gorpc.Materialization(
            tunnel.MaterializationRequest(project_id=self.__project_id, material_ref=self.__material_ref))
        return json_format.MessageToDict(mznResponse.materialization)

    def encapsulating_model(self):
        """
        Get the encapsulating model of the model

        Returns:
            WhtModel: encapsulating model
        """
        encapsulatingMaterialResponse: tunnel.EncapsulatingMaterialResponse = self.__gorpc.EncapsulatingMaterial(
            tunnel.EncapsulatingMaterialRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return WhtModel(self.__project_id, encapsulatingMaterialResponse.encapsulating_material_ref)

    def entity(self) -> Optional[Dict]:
        """
        Get the entity of the model

        Returns:
            Dict: Entity of the model
        """
        entityResponse: tunnel.EntityResponse = self.__gorpc.Entity(
            tunnel.EntityRequest(project_id=self.__project_id, material_ref=self.__material_ref))
        entity = json_format.MessageToDict(entityResponse.entity)
        if len(entity) == 0:  # empty dict
            return None

        return entity

    def get_description(self) -> Optional[str]:
        descriptionResponse: tunnel.GetVarDescriptionResponse = self.__gorpc.GetVarDescription(
            tunnel.GetVarDescriptionRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return descriptionResponse.description


class WhtMaterial:
    _wht_ctx_store = WhtContextStore()

    def __init__(self, project_id: int, material_ref: int, output_folder_suffix: Literal["compile", "run"]):
        self.__project_id = project_id
        self.__material_ref = material_ref
        self.__gorpc = get_gorpc()
        self.__output_folder_suffix = output_folder_suffix
        self.model = WhtModel(project_id, material_ref)
        self.base_wht_project = BaseWhtProject(project_id, material_ref)

        self.wht_ctx = self._wht_ctx_store.get_context(
            project_id, material_ref)

        self.logger = Logger("WhtMaterial")

    def string(self) -> str:
        """Get the standardized table name of the material. It should return a string that can be used in SQL."""
        string_res: tunnel.MaterialStringResponse = self.__gorpc.MaterialString(
            tunnel.MaterialStringRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return string_res.material_string

    def name(self) -> str:
        """Get the name of the material

        Returns:
            str: Name of the material
        """
        name_res: tunnel.NameResponse = self.__gorpc.Name(
            tunnel.NameRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return name_res.material_name

    def get_output_folder(self) -> str:
        """Get the output folder path of the material

        Returns:
            str: Output folder of the material
        """
        output_folder_res: tunnel.OutputFolderResponse = self.__gorpc.OutputFolder(
            tunnel.OutputFolderRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return path.join(output_folder_res.output_folder, self.__output_folder_suffix)

    def build_contract(self, contract: Union[str, Dict[Any, Any]]) -> Contract:
        """Builds a contract from a string or a dict

        Args:
            contract (str): The contract to be built

        Returns:
            Contract: The built contract
        """
        if isinstance(contract, dict):
            contract = json.dumps(contract)

        contract_res: tunnel.BuildContractResponse = self.__gorpc.BuildContract(
            tunnel.BuildContractRequest(contract=contract, project_id=self.__project_id))
        return Contract(contract_res.contract_ref)

    def de_ref(self, model_path: Optional[str] = None, **kwargs):
        """Dereference a material

        Args:
            model_path (str): Path to the model

        Keyword Args:
            edge_type (str): Edge type - normal, preferred or optional
            contract (Contract): Contract to be used
            pre_existing (bool): if true we search for pre-existing materials from material registry
            allow_incomplete_materials (bool): materials with complete status as complete(2) as well as incomplete(3)
            remember_context_as (str): saves the context of past/previous material in material registry entry of this material

        Returns:
            WhtMaterial: Dereferenced material
        """
        edge_type = kwargs.get("edge_type", None)
        contract = kwargs.get("contract", None)
        contract_ref = contract.ref() if contract is not None else None
        pre_existing = kwargs.get("pre_existing", None)
        allow_incomplete_materials = kwargs.get(
            "allow_incomplete_materials", None)
        remember_context_as = kwargs.get("remember_context_as", None)

        de_ref_res: tunnel.DeRefResponse = self.__gorpc.DeRef(tunnel.DeRefRequest(
            project_id=self.__project_id,
            material_ref=self.__material_ref,
            model_path=model_path,
            edge_type=edge_type,
            contract_ref=contract_ref,
            pre_existing=pre_existing,
            allow_incomplete_materials=allow_incomplete_materials,
            remember_context_as=remember_context_as,
        ))
        if de_ref_res.is_null:
            return None

        return WhtMaterial(self.__project_id, de_ref_res.material_ref, self.__material_ref)

    def get_columns(self):
        """Get the columns of the material

        Returns:
            List[dict]: List of columns
        """
        get_columns_res: tunnel.GetColumnsResponse = self.__gorpc.GetColumns(
            tunnel.GetColumnsRequest(project_id=self.__project_id, material_ref=self.__material_ref))

        return [{"name": col.name, "type": col.type} for col in get_columns_res.columns]

    def get_df(self, select_columns: Optional[List[str]] = None, batching=False, batch_size=100000):
        """Get the table data of the material.

        Args:
            select_columns (List[str], optional): List of columns to be selected. Defaults to None.
            batching (bool, optional): Whether to use batching. Defaults to False.
            batch_size (int, optional): Batch size(not supported for snowpark). Defaults to 100000.

        Returns:
            DataFrame: Table data as DataFrame or Iterable[DataFrame]
        """
        get_selector_sql = self.__gorpc.GetSelectorSql(tunnel.GetSelectorSqlRequest(
            project_id=self.__project_id, material_ref=self.__material_ref, columns=select_columns))

        return self.wht_ctx.client.get_df(get_selector_sql.sql, batching, batch_size)

    def get_snowpark_df(self, select_columns: Optional[List[str]] = None):
        """Get the table data of the material as Snowpark DataFrame.

        Args:
            select_columns (List[str], optional): List of columns to be selected. Defaults to None.

        Returns:
            DataFrame: Table data as Snowpark DataFrame
        """
        get_selector_sql = self.__gorpc.GetSelectorSql(tunnel.GetSelectorSqlRequest(
            project_id=self.__project_id, material_ref=self.__material_ref, columns=select_columns))

        return self.wht_ctx.client.get_snowpark_df(get_selector_sql.sql)

    def write_output(self, df: pd.DataFrame, append_if_exists: bool = False):
        """Write the dataframe as the output of the material

        Args:
            df (pd.DataFrame): DataFrame to be written
            append_if_exists (bool, optional): Append to the table if it exists. Defaults to False.
        """
        table_name = self.string()  # standardized table name
        schema = ""
        if "." in table_name:
            schema, table_name = table_name.split(".")

        self.wht_ctx.client.write_df_to_table(
            df, table_name, schema, append_if_exists)

    def execute_text_template(self, template: str) -> str:
        template_res: tunnel.ExecuteTextTemplateResponse = self.__gorpc.ExecuteTextTemplate(
            tunnel.ExecuteTextTemplateRequest(project_id=self.__project_id,  material_ref=self.__material_ref, template=template))

        return template_res.result
