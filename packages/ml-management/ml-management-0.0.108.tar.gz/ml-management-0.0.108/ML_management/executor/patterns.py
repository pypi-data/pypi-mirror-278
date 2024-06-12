"""Module with patterns for models parameters in executors."""
from typing import Dict, List

from pydantic import BaseModel, root_validator

from ML_management.executor.upload_model_mode import UploadModelMode
from ML_management.model.model_type_to_methods_map import ModelMethodName


class OneModelPattern(BaseModel):
    """Pattern for only one model."""

    upload_model_modes: UploadModelMode
    desired_model_methods: List[ModelMethodName]


class ArbitraryModelsPattern(BaseModel):
    """Pattern for arbitrary number of models."""

    upload_model_modes: Dict[str, UploadModelMode]
    desired_model_methods: Dict[str, List[ModelMethodName]]

    @root_validator(skip_on_failure=True)
    @classmethod
    def check_dicts_consistent(cls, values):
        upload_model_mode_keys = set(values["upload_model_modes"].keys())
        desired_model_methods_keys = set(values["desired_model_methods"].keys())
        assert (
            upload_model_mode_keys == desired_model_methods_keys
        ), "desired_model_methods and upload_model_mode must have the same model roles"
        return values
