from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.index import Index


T = TypeVar("T", bound="IndexInSpec")


@_attrs_define
class IndexInSpec:
    """
    Attributes:
        collection_name (str):
        field_name (str):
        index (Index):
        object_type (Union[Literal['IndexInSpec'], Unset]):  Default: 'IndexInSpec'.
    """

    collection_name: str
    field_name: str
    index: "Index"
    object_type: Union[Literal["IndexInSpec"], Unset] = "IndexInSpec"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name

        field_name = self.field_name

        index = self.index.to_dict()

        object_type = self.object_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "field_name": field_name,
                "index": index,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.index import Index

        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        field_name = d.pop("field_name")

        index = Index.from_dict(d.pop("index"))

        object_type = d.pop("object_type", UNSET)

        index_in_spec = cls(
            collection_name=collection_name,
            field_name=field_name,
            index=index,
            object_type=object_type,
        )

        index_in_spec.additional_properties = d
        return index_in_spec

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
