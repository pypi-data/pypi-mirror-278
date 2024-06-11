import datetime
from typing import Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrashCanEntry")


@_attrs_define
class TrashCanEntry:
    """
    Attributes:
        collection (str):
        data_collection_primary_key (str):
        soft_deletion_timestamp (datetime.datetime):
        soft_deleter (str):
        link (str):
        object_type (Union[Literal['TrashCanEntry'], Unset]):  Default: 'TrashCanEntry'.
    """

    collection: str
    data_collection_primary_key: str
    soft_deletion_timestamp: datetime.datetime
    soft_deleter: str
    link: str
    object_type: Union[Literal["TrashCanEntry"], Unset] = "TrashCanEntry"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection = self.collection

        data_collection_primary_key = self.data_collection_primary_key

        soft_deletion_timestamp = self.soft_deletion_timestamp.isoformat()

        soft_deleter = self.soft_deleter

        link = self.link

        object_type = self.object_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
                "data_collection_primary_key": data_collection_primary_key,
                "soft_deletion_timestamp": soft_deletion_timestamp,
                "soft_deleter": soft_deleter,
                "link": link,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection = d.pop("collection")

        data_collection_primary_key = d.pop("data_collection_primary_key")

        soft_deletion_timestamp = isoparse(d.pop("soft_deletion_timestamp"))

        soft_deleter = d.pop("soft_deleter")

        link = d.pop("link")

        object_type = d.pop("object_type", UNSET)

        trash_can_entry = cls(
            collection=collection,
            data_collection_primary_key=data_collection_primary_key,
            soft_deletion_timestamp=soft_deletion_timestamp,
            soft_deleter=soft_deleter,
            link=link,
            object_type=object_type,
        )

        trash_can_entry.additional_properties = d
        return trash_can_entry

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
