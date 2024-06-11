from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InputData")


@_attrs_define
class InputData:
    """
    Attributes:
        collection_name (str):
        data (List[List[Any]]):
        object_type (Union[Literal['InputData'], Unset]):  Default: 'InputData'.
    """

    collection_name: str
    data: List[List[Any]]
    object_type: Union[Literal["InputData"], Unset] = "InputData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name

        data = []
        for data_item_data in self.data:
            data_item = data_item_data

            data.append(data_item)

        object_type = self.object_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "data": data,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = cast(List[Any], data_item_data)

            data.append(data_item)

        object_type = d.pop("object_type", UNSET)

        input_data = cls(
            collection_name=collection_name,
            data=data,
            object_type=object_type,
        )

        input_data.additional_properties = d
        return input_data

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
