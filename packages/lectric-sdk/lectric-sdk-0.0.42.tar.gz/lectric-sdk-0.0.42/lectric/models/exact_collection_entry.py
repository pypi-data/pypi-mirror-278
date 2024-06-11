import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exact_collection_entry_metadata import ExactCollectionEntryMetadata


T = TypeVar("T", bound="ExactCollectionEntry")


@_attrs_define
class ExactCollectionEntry:
    """
    Attributes:
        id (str):
        link (str):
        timestamp (datetime.datetime):
        is_file_upload (bool):
        metadata (ExactCollectionEntryMetadata):
        is_marked_for_deletion (bool):
        ingestor (str):
        fk (str):
        object_type (Union[Literal['ExactCollectionEntry'], Unset]):  Default: 'ExactCollectionEntry'.
    """

    id: str
    link: str
    timestamp: datetime.datetime
    is_file_upload: bool
    metadata: "ExactCollectionEntryMetadata"
    is_marked_for_deletion: bool
    ingestor: str
    fk: str
    object_type: Union[Literal["ExactCollectionEntry"], Unset] = "ExactCollectionEntry"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        link = self.link

        timestamp = self.timestamp.isoformat()

        is_file_upload = self.is_file_upload

        metadata = self.metadata.to_dict()

        is_marked_for_deletion = self.is_marked_for_deletion

        ingestor = self.ingestor

        fk = self.fk

        object_type = self.object_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "link": link,
                "timestamp": timestamp,
                "is_file_upload": is_file_upload,
                "metadata": metadata,
                "is_marked_for_deletion": is_marked_for_deletion,
                "ingestor": ingestor,
                "fk": fk,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.exact_collection_entry_metadata import ExactCollectionEntryMetadata

        d = src_dict.copy()
        id = d.pop("id")

        link = d.pop("link")

        timestamp = isoparse(d.pop("timestamp"))

        is_file_upload = d.pop("is_file_upload")

        metadata = ExactCollectionEntryMetadata.from_dict(d.pop("metadata"))

        is_marked_for_deletion = d.pop("is_marked_for_deletion")

        ingestor = d.pop("ingestor")

        fk = d.pop("fk")

        object_type = d.pop("object_type", UNSET)

        exact_collection_entry = cls(
            id=id,
            link=link,
            timestamp=timestamp,
            is_file_upload=is_file_upload,
            metadata=metadata,
            is_marked_for_deletion=is_marked_for_deletion,
            ingestor=ingestor,
            fk=fk,
            object_type=object_type,
        )

        exact_collection_entry.additional_properties = d
        return exact_collection_entry

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
