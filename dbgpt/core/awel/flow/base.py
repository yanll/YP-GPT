"""The mixin of DAGs."""
import dataclasses
import inspect
from abc import ABC
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

from dbgpt._private.pydantic import BaseModel, Field, root_validator
from dbgpt.core.interface.serialization import Serializable

_TYPE_REGISTRY: Dict[str, Type] = {}


_ALLOWED_TYPES: Dict[str, Type] = {
    "str": str,
    "int": int,
}

_BASIC_TYPES = [str, int, float, bool, dict, list, set]

T = TypeVar("T", bound="ViewMixin")


def _get_type_name(type_: Type[Any]) -> str:
    """Get the type name of the type.

    Register the type if the type is not registered.

    Args:
        type_ (Type[Any]): The type.

    Returns:
        str: The type na
    """
    type_name = f"{type_.__module__}.{type_.__qualname__}"

    if type_name not in _TYPE_REGISTRY:
        _TYPE_REGISTRY[type_name] = type_

    return type_name


def _get_type_cls(type_name: str) -> Type[Any]:
    """Get the type class by the type name.

    Args:
        type_name (str): The type name.

    Returns:
        Type[Any]: The type class.

    Raises:
        ValueError: If the type is not registered.
    """
    if type_name not in _TYPE_REGISTRY:
        raise ValueError(f"Type {type_name} not registered.")
    return _TYPE_REGISTRY[type_name]


# Register the basic types.
for t in _BASIC_TYPES:
    _get_type_name(t)


class _MISSING_TYPE:
    pass


_MISSING_VALUE = _MISSING_TYPE()


def _serialize_complex_obj(obj: Any) -> Any:
    if isinstance(obj, Serializable):
        return obj.to_dict()
    elif dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj


def _serialize_recursive(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: _serialize_complex_obj(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_serialize_complex_obj(item) for item in data]
    else:
        return _serialize_complex_obj(data)


class OptionValue(Serializable, BaseModel):
    """The option value of the parameter."""

    label: str = Field(..., description="The label of the option")
    name: str = Field(..., description="The name of the option")
    value: Any = Field(..., description="The value of the option")

    def to_dict(self) -> Dict:
        """Convert current metadata to json dict."""
        return self.dict()


class ParameterType(str, Enum):
    """The type of the parameter."""

    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DICT = "dict"
    LIST = "list"


class ParameterCategory(str, Enum):
    """The category of the parameter."""

    COMMON = "common"
    RESOURCER = "resource"

    @classmethod
    def values(cls) -> List[str]:
        """Get the values of the category."""
        return [category.value for category in cls]

    @classmethod
    def get_category(cls, value: Type[Any]) -> "ParameterCategory":
        """Get the category of the value.

        Args:
            value (Any): The value.

        Returns:
            ParameterCategory: The category of the value.
        """
        if value in _BASIC_TYPES:
            return cls.COMMON
        else:
            return cls.RESOURCER


DefaultParameterType = Union[str, int, float, bool, None]


class TypeMetadata(BaseModel):
    """The metadata of the type."""

    type_name: str = Field(..., description="The type short name of the parameter")

    type_cls: str = Field(..., description="The type class of the parameter")


class Parameter(TypeMetadata, Serializable):
    """Parameter for build operator."""

    label: str = Field(..., description="The label to display in UI")
    name: str = Field(..., description="The name of the parameter")
    category: str = Field(
        ...,
        description="The category of the parameter",
        examples=["common", "resource"],
    )
    optional: bool = Field(..., description="Whether the parameter is optional")
    default: Optional[DefaultParameterType] = Field(
        None, description="The default value of the parameter"
    )
    placeholder: Optional[DefaultParameterType] = Field(
        None, description="The placeholder of the parameter"
    )
    description: Optional[str] = Field(
        None, description="The description of the parameter"
    )
    options: Optional[List[OptionValue]] = Field(
        None, description="The options of the parameter"
    )
    value: Optional[Any] = Field(
        None, description="The value of the parameter(Saved in the dag file)"
    )

    @classmethod
    def build_from(
        cls,
        label: str,
        name: str,
        type: Type,
        optional: bool = False,
        default: Optional[Union[DefaultParameterType, _MISSING_TYPE]] = _MISSING_VALUE,
        placeholder: Optional[DefaultParameterType] = None,
        description: Optional[str] = None,
        options: Optional[List[OptionValue]] = None,
    ):
        """Build the parameter from the type."""
        type_name = type.__qualname__
        type_cls = _get_type_name(type)
        category = ParameterCategory.get_category(type)
        if optional and default == _MISSING_VALUE:
            raise ValueError(f"Default value is missing for optional parameter {name}.")
        if not optional:
            default = None
        return cls(
            label=label,
            name=name,
            type_name=type_name,
            type_cls=type_cls,
            category=category.value,
            optional=optional,
            default=default,
            placeholder=placeholder,
            description=description or label,
            options=options,
        )

    @classmethod
    def build_from_ui(cls, data: Dict) -> "Parameter":
        """Build the parameter from the type.

        Some fields are not trusted, so we need to check the type.

        Args:
            data (Dict): The parameter data.

        Returns:
            Parameter: The parameter.
        """
        type_str = data["type_cls"]
        type_name = data["type_name"]
        # Build and check the type.
        category = ParameterCategory.get_category(_get_type_cls(type_str))
        return cls(
            label=data["label"],
            name=data["name"],
            type_name=type_name,
            type_cls=type_str,
            category=category.value,
            optional=data["optional"],
            default=data["default"],
            description=data["description"],
            options=data["options"],
            value=data["value"],
        )

    def to_dict(self) -> Dict:
        """Convert current metadata to json dict."""
        return self.dict()

    def to_runnable_parameter(
        self,
        view_value: Any,
        resources: Optional[Dict[str, "ResourceMetadata"]] = None,
    ) -> Dict:
        """Convert the parameter to runnable parameter.

        Args:
            view_value (Any): The value from UI.
            resources (Optional[Dict[str, "ResourceMetadata"]], optional):
                The resources. Defaults to None.

        Returns:
            Dict: The runnable parameter.
        """
        if view_value and self.category == ParameterCategory.RESOURCER and resources:
            # Resource type can have multiple parameters.
            resource_id = view_value
            resource_metadata = resources[resource_id]
            # Check the type.
            resource_type = _get_type_cls(resource_metadata.type_cls)
            resource_kwargs = {}
            for parameter in resource_metadata.parameters:
                resource_kwargs[parameter.name] = parameter.value
            value = resource_type(**resource_kwargs)
        else:
            value = view_value or self.value or self.default
        return {self.name: value}


class BaseResource(Serializable, BaseModel):
    """The base resource."""

    label: str = Field(..., description="The label to display in UI")
    name: str = Field(..., description="The name of the operator")
    description: str = Field(..., description="The description of the field")

    def to_dict(self) -> Dict:
        """Convert current metadata to json dict."""
        return self.dict()


class Resource(BaseResource, TypeMetadata):
    """The resource of the operator."""

    @classmethod
    def build_from(
        cls, label: str, name: str, type: Type, description: Optional[str] = None
    ):
        """Build the resource from the type."""
        type_name = type.__qualname__
        type_cls = _get_type_name(type)
        return cls(
            label=label,
            name=name,
            type_name=type_name,
            type_cls=type_cls,
            description=description or label,
        )


class IOFiledType(str, Enum):
    """The type of the input or output field."""

    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DICT = "dict"
    LIST = "list"


class IOField(Resource):
    """The input or output field of the operator."""

    pass


class OperatorCategory(str, Enum):
    """The category of the operator."""

    TRIGGER = "trigger"
    LLM = "llm"
    CONVERSION = "conversion"
    OUTPUT_PARSER = "output_parser"
    COMMON = "common"


class ResourceCategory(str, Enum):
    """The category of the resource."""

    LLM_CLIENT = "llm_client"
    COMMON = "common"


class BaseMetadata(BaseResource):
    """The base metadata."""

    category: str = Field(..., description="The category of the operator")

    flow_type: Optional[str] = Field(
        ..., description="The flow type", examples=["operator", "resource"]
    )
    icon: Optional[str] = Field(
        default=None,
        description="The icon of the operator or resource",
        examples=["public/awel/icons/llm.svg"],
    )
    documentation_url: Optional[str] = Field(
        default=None,
        description="The documentation url of the operator or resource",
        examples=["https://docs.dbgpt.site/docs/awel"],
    )

    key: str = Field(
        description="The key of the operator or resource",
    )

    tags: Optional[List[str]] = Field(
        default=None,
        description="The tags of the operator",
        examples=[["llm", "openai", "gpt3"]],
    )

    parameters: List[Parameter] = Field(
        ..., description="The parameters of the operator or resource"
    )

    @property
    def is_operator(self) -> bool:
        """Whether the metadata is for operator."""
        return self.flow_type == "operator"

    def get_runnable_parameters(
        self,
        view_parameters: Optional[List[Parameter]],
        resources: Optional[Dict[str, "ResourceMetadata"]] = None,
    ) -> Dict:
        """Get the runnable parameters.

        Args:
            view_parameters (Optional[List[Parameter]]):
                The parameters from UI.
            resources (Optional[Dict[str, "ResourceMetadata"]], optional):
                The resources. Defaults to None.

        Returns:
            Dict: The runnable parameters.
        """
        runnable_parameters: Dict[str, Any] = {}
        if not self.parameters or not view_parameters:
            return runnable_parameters
        if len(self.parameters) != len(view_parameters):
            raise ValueError(
                f"Parameters count not match. "
                f"Expected {len(self.parameters)}, but got {len(view_parameters)}."
            )
        for i, parameter in enumerate(self.parameters):
            view_param = view_parameters[i]
            runnable_parameters.update(
                parameter.to_runnable_parameter(view_param.value, resources)
            )
        return runnable_parameters


class ResourceMetadata(BaseMetadata, TypeMetadata):
    """The metadata of the resource."""

    parent_cls: List[str] = Field(
        default_factory=list, description="The parent class of the resource"
    )

    @root_validator(pre=True)
    def pre_fill(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Pre fill the metadata."""
        if "flow_type" not in values:
            values["flow_type"] = "resource"
        if "key" not in values:
            values["key"] = values["flow_type"] + "_" + values["type_cls"]
        return values


def register_resource(
    label: str,
    name: Optional[str] = None,
    category: str = "common",
    parameters: Optional[List[Parameter]] = None,
    description: Optional[str] = None,
    **kwargs,
):
    """Register the resource.

    Args:
        label (str): The label of the resource.
        name (Optional[str], optional): The name of the resource. Defaults to None.
        category (str, optional): The category of the resource. Defaults to "common".
        parameters (Optional[List[Parameter]], optional): The parameters of the
            resource. Defaults to None.
        description (Optional[str], optional): The description of the resource.
            Defaults to None.
    """

    def decorator(cls):
        """Wrap the class."""
        resource_description = description or cls.__doc__
        # Register the type
        type_name = cls.__qualname__
        type_cls = _get_type_name(cls)
        mro = inspect.getmro(cls)
        parent_cls = [
            _get_type_name(parent_cls)
            for parent_cls in mro
            if parent_cls != object and parent_cls != cls
        ]

        resource_metadata = ResourceMetadata(
            label=label,
            name=name or type_name,
            category=category,
            description=resource_description or label,
            type_name=type_name,
            type_cls=type_cls,
            parameters=parameters or [],
            parent_cls=parent_cls,
            **kwargs,
        )
        _register_resource(cls, resource_metadata)

        # Attach the metadata to the class
        cls._resource_metadata = resource_metadata
        return cls

    return decorator


class ViewMetadata(BaseMetadata):
    """The metadata of the operator.

    We use this metadata to build the operator in UI and view the operator in UI.
    """

    inputs: List[IOField] = Field(..., description="The inputs of the operator")
    outputs: List[IOField] = Field(..., description="The outputs of the operator")
    version: str = Field(default="v1", description="The version of the operator")

    @root_validator(pre=True)
    def pre_fill(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Pre fill the metadata."""
        if "flow_type" not in values:
            values["flow_type"] = "operator"
        if "key" not in values:
            key = cls.get_key(
                values["name"], values["category"], values.get("version", "v1")
            )
            values["key"] = values["flow_type"] + "_" + key
        return values

    def get_operator_key(self) -> str:
        """Get the operator key."""
        if not self.flow_type:
            raise ValueError("Flow type can't be empty")
        return (
            self.flow_type + "_" + self.get_key(self.name, self.category, self.version)
        )

    @staticmethod
    def get_key(name: str, category: str, version: str) -> str:
        """Get the operator key."""
        split_str = "___$$___"
        return f"{name}{split_str}{category}{split_str}{version}"


class ViewMixin(ABC):
    """The mixin of the operator."""

    metadata: Optional[ViewMetadata] = None

    def get_view_metadata(self) -> Optional[ViewMetadata]:
        """Get the view metadata.

        Returns:
            Optional[ViewMetadata]: The view metadata.
        """
        return self.metadata

    @classmethod
    def after_define(cls):
        """After define the operator, register the operator."""
        _register_operator(cls)

    def to_dict(self) -> Dict:
        """Convert current metadata to json.

        Show the metadata in UI.

        Returns:
            Dict: The metadata dict.

        Raises:
            ValueError: If the metadata is not set.
        """
        metadata = self.get_view_metadata()
        if not metadata:
            raise ValueError("Metadata is not set.")
        metadata_dict = metadata.to_dict()
        return metadata_dict

    @classmethod
    def build_from(
        cls: Type[T],
        view_metadata: ViewMetadata,
        key_to_resource: Optional[Dict[str, "ResourceMetadata"]] = None,
    ) -> T:
        """Build the operator from the metadata."""
        operator_key = view_metadata.get_operator_key()
        operator_cls: Type[T] = _get_operator_class(operator_key)
        metadata = operator_cls.metadata
        if not metadata:
            raise ValueError("Metadata is not set.")
        runnable_params = metadata.get_runnable_parameters(
            view_metadata.parameters, key_to_resource
        )
        operator_task: T = operator_cls(**runnable_params)
        return operator_task


@dataclasses.dataclass
class _RegistryItem:
    """The registry item."""

    key: str
    cls: Type
    metadata: Union[ViewMetadata, ResourceMetadata]


class FlowRegistry:
    """The registry of the operator and resource."""

    def __init__(self):
        """Init the registry."""
        self._registry: Dict[str, _RegistryItem] = {}

    def register_flow(
        self, view_cls: Type, metadata: Union[ViewMetadata, ResourceMetadata]
    ):
        """Register the operator."""
        key = metadata.key
        self._registry[key] = _RegistryItem(key=key, cls=view_cls, metadata=metadata)

    def get_registry_item(self, key: str) -> Optional[_RegistryItem]:
        """Get the registry item by the key."""
        return self._registry.get(key)

    def metadata_list(self) -> List[Union[ViewMetadata, ResourceMetadata]]:
        """Get the metadata list."""
        return [item.metadata for item in self._registry.values()]


_OPERATOR_REGISTRY: FlowRegistry = FlowRegistry()


def _get_operator_class(type_key: str) -> Type[T]:
    """Get the operator class by the type name."""
    item = _OPERATOR_REGISTRY.get_registry_item(type_key)
    if not item:
        raise ValueError(f"Operator {type_key} not registered.")
    cls = item.cls
    if not issubclass(cls, ViewMixin):
        raise ValueError(f"Operator {type_key} is not a ViewMixin.")
    return cast(Type[T], cls)


def _register_operator(view_cls: Optional[Type[T]]):
    """Register the operator."""
    if not view_cls or not view_cls.metadata:
        return
    metadata = view_cls.metadata
    _OPERATOR_REGISTRY.register_flow(view_cls, metadata)


def _get_resource_class(type_key: str) -> ResourceMetadata:
    """Get the operator class by the type name."""
    item = _OPERATOR_REGISTRY.get_registry_item(type_key)
    if not item:
        raise ValueError(f"Resource {type_key} not registered.")
    if not isinstance(item.metadata, ResourceMetadata):
        raise ValueError(f"Resource {type_key} is not a ResourceMetadata.")
    return item.metadata


def _register_resource(cls: Type, resource_metadata: ResourceMetadata):
    """Register the operator."""
    _OPERATOR_REGISTRY.register_flow(cls, resource_metadata)