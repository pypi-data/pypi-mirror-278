# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union
from uuid import uuid4

from marimo._ast.cell import CellId_t
from marimo._config.config import MarimoConfig

UIElementId = str
CompletionRequestId = str
FunctionCallId = str

T = TypeVar("T")
ListOrValue = Union[T, List[T]]
SerializedQueryParams = Dict[str, ListOrValue[str]]
Primitive = Union[str, bool, int, float]
SerializedCLIArgs = Dict[str, ListOrValue[Union[Primitive]]]


@dataclass
class ExecutionRequest:
    cell_id: CellId_t
    code: str


@dataclass
class ExecuteStaleRequest: ...


@dataclass
class ExecuteMultipleRequest:
    execution_requests: List[ExecutionRequest]


@dataclass
class SetUIElementValueRequest:
    # (object id, value) tuples
    ids_and_values: List[Tuple[UIElementId, Any]]
    # uniquely identifies the request
    token: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class FunctionCallRequest:
    function_call_id: FunctionCallId
    namespace: str
    function_name: str
    args: Dict[str, Any]


@dataclass
class AppMetadata:
    """Hold metadata about the app, like its filename."""

    query_params: SerializedQueryParams
    cli_args: SerializedCLIArgs

    filename: Optional[str] = None


@dataclass
class SetCellConfigRequest:
    # Map from Cell ID to (possibly partial) CellConfig
    configs: Dict[CellId_t, Dict[str, object]]


@dataclass
class SetUserConfigRequest:
    # MarimoConfig TypedDict
    config: MarimoConfig


@dataclass
class CreationRequest:
    execution_requests: Tuple[ExecutionRequest, ...]
    set_ui_element_value_request: SetUIElementValueRequest


@dataclass
class DeleteRequest:
    cell_id: CellId_t


@dataclass
class StopRequest:
    pass


@dataclass
class CompletionRequest:
    id: CompletionRequestId
    document: str
    cell_id: CellId_t


@dataclass
class InstallMissingPackagesRequest:
    # TODO: package manager (pip/conda/...), index URL (index/channel/...)
    manager: str


@dataclass
class PreviewDatasetColumnRequest:
    # The source of the dataset
    source: str
    # The name of the dataset
    # This currently corresponds to the variable name
    table_name: str
    # The name of the column
    column_name: str


ControlRequest = Union[
    ExecuteMultipleRequest,
    ExecuteStaleRequest,
    CreationRequest,
    DeleteRequest,
    FunctionCallRequest,
    SetCellConfigRequest,
    SetUserConfigRequest,
    SetUIElementValueRequest,
    StopRequest,
    InstallMissingPackagesRequest,
    PreviewDatasetColumnRequest,
]
