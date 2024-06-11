from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldSchema")


@_attrs_define
class FieldSchema:
    """
    Attributes:
        name (str):
        dtype (int):
        object_type (Union[Literal['FieldSchema'], Unset]):  Default: 'FieldSchema'.
        is_primary (Union[None, Unset, bool]):  Default: False.
        auto_id (Union[None, Unset, bool]):  Default: False.
        description (Union[None, Unset, str]):  Default: ''.
        dim (Union[None, Unset, int]):
        max_length (Union[None, Unset, int]):
    """

    name: str
    dtype: int
    object_type: Union[Literal["FieldSchema"], Unset] = "FieldSchema"
    is_primary: Union[None, Unset, bool] = False
    auto_id: Union[None, Unset, bool] = False
    description: Union[None, Unset, str] = ""
    dim: Union[None, Unset, int] = UNSET
    max_length: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        dtype = self.dtype

        object_type = self.object_type

        is_primary: Union[None, Unset, bool]
        if isinstance(self.is_primary, Unset):
            is_primary = UNSET
        else:
            is_primary = self.is_primary

        auto_id: Union[None, Unset, bool]
        if isinstance(self.auto_id, Unset):
            auto_id = UNSET
        else:
            auto_id = self.auto_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        dim: Union[None, Unset, int]
        if isinstance(self.dim, Unset):
            dim = UNSET
        else:
            dim = self.dim

        max_length: Union[None, Unset, int]
        if isinstance(self.max_length, Unset):
            max_length = UNSET
        else:
            max_length = self.max_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "dtype": dtype,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if is_primary is not UNSET:
            field_dict["is_primary"] = is_primary
        if auto_id is not UNSET:
            field_dict["auto_id"] = auto_id
        if description is not UNSET:
            field_dict["description"] = description
        if dim is not UNSET:
            field_dict["dim"] = dim
        if max_length is not UNSET:
            field_dict["max_length"] = max_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        dtype = d.pop("dtype")

        object_type = d.pop("object_type", UNSET)

        def _parse_is_primary(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_primary = _parse_is_primary(d.pop("is_primary", UNSET))

        def _parse_auto_id(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        auto_id = _parse_auto_id(d.pop("auto_id", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_dim(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        dim = _parse_dim(d.pop("dim", UNSET))

        def _parse_max_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_length = _parse_max_length(d.pop("max_length", UNSET))

        field_schema = cls(
            name=name,
            dtype=dtype,
            object_type=object_type,
            is_primary=is_primary,
            auto_id=auto_id,
            description=description,
            dim=dim,
            max_length=max_length,
        )

        field_schema.additional_properties = d
        return field_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
