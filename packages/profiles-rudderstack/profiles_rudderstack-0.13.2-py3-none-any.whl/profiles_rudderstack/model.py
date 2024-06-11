from ctypes import Union
from typing import Tuple, Optional, List, Union
from abc import ABC, abstractmethod
from profiles_rudderstack.recipe import PyNativeRecipe
from typing import NamedTuple, Dict, Any


class MaterializationSpec(NamedTuple):
    output_type: str
    run_type: str
    requested_enable_status: str


class EntityId(NamedTuple):
    select: str = ""
    type: str = ""
    entity: str = ""
    to_default_stitcher: bool = False


class BaseModelType(ABC):
    TypeName = "base_model_type"
    # Json Schema
    BuildSpecSchema = {}

    contract: Optional[Union[str, Dict[str, Any]]] = None
    entity_key: Optional[str] = None
    materialization: Optional[MaterializationSpec] = None
    ids: Optional[List[EntityId]] = None

    def __init__(self, build_spec: Dict[Any, Any], schema_version: int, pb_version: str) -> None:
        self.build_spec = build_spec
        self.schema_version = schema_version
        self.pb_version = pb_version

        if build_spec.get("entity_key", None) is not None:
            self.entity_key = build_spec["entity_key"]

        if build_spec.get("time_grain", None) is not None:
            self.time_grain = build_spec["time_grain"]

        if build_spec.get("contract", None) is not None:
            self.contract = build_spec["contract"]

        mzn = build_spec.get("materialization", None)
        if mzn is not None:
            self.materialization = MaterializationSpec(mzn.get(
                "output_type", ""), mzn.get("run_type", ""), mzn.get("enable_status", ""))

        if build_spec.get("ids", None) is not None:
            self.ids = []
            for id in build_spec["ids"]:
                self.ids.append(EntityId(
                    id["select"], id["type"], id["entity"], id.get("to_default_stitcher", False)))

    @abstractmethod
    def get_material_recipe(self) -> PyNativeRecipe:
        """Define the material recipe of the model

        Returns:
            Recipe: Material recipe of the model
        """
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> Tuple[bool, str]:
        """Validate the model

        Returns:
            Tuple[bool, str]: Validation result and error message
        """
        if self.schema_version < 43:
            return False, "schema version should >= 43"
        return True, ""

    def get_db_object_name_suffix(self) -> (str):
        return ""
