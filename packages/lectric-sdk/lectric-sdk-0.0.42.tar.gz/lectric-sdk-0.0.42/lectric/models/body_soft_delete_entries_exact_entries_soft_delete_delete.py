from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodySoftDeleteEntriesExactEntriesSoftDeleteDelete")


@_attrs_define
class BodySoftDeleteEntriesExactEntriesSoftDeleteDelete:
    """
    Attributes:
        entry_ids (Union[List[int], List[str], Unset]):
        urls (Union[Unset, List[str]]):
    """

    entry_ids: Union[List[int], List[str], Unset] = UNSET
    urls: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entry_ids: Union[List[int], List[str], Unset]
        if isinstance(self.entry_ids, Unset):
            entry_ids = UNSET
        elif isinstance(self.entry_ids, list):
            entry_ids = self.entry_ids

        else:
            entry_ids = self.entry_ids

        urls: Union[Unset, List[str]] = UNSET
        if not isinstance(self.urls, Unset):
            urls = self.urls

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entry_ids is not UNSET:
            field_dict["entry_ids"] = entry_ids
        if urls is not UNSET:
            field_dict["urls"] = urls

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_entry_ids(data: object) -> Union[List[int], List[str], Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entry_ids_type_0 = cast(List[int], data)

                return entry_ids_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            entry_ids_type_1 = cast(List[str], data)

            return entry_ids_type_1

        entry_ids = _parse_entry_ids(d.pop("entry_ids", UNSET))

        urls = cast(List[str], d.pop("urls", UNSET))

        body_soft_delete_entries_exact_entries_soft_delete_delete = cls(
            entry_ids=entry_ids,
            urls=urls,
        )

        body_soft_delete_entries_exact_entries_soft_delete_delete.additional_properties = d
        return body_soft_delete_entries_exact_entries_soft_delete_delete

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
