from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryMetaParams")


@_attrs_define
class QueryMetaParams:
    """
    Attributes:
        nprobe (int): Number of units to query. CPU: [1, nlist], GPU: [1, min(2048, nlist)
        object_type (Union[Literal['QueryMetaParams'], Unset]):  Default: 'QueryMetaParams'.
        ef (Union[None, Unset, int]): Search Scope. Range [top_k, 32768]
        search_k (Union[None, Unset, int]): The number of nodes to search. -1 means 5% of the whole data. Range {-1} U
            [top_k, n x n_trees]
    """

    nprobe: int
    object_type: Union[Literal["QueryMetaParams"], Unset] = "QueryMetaParams"
    ef: Union[None, Unset, int] = UNSET
    search_k: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        nprobe = self.nprobe

        object_type = self.object_type

        ef: Union[None, Unset, int]
        if isinstance(self.ef, Unset):
            ef = UNSET
        else:
            ef = self.ef

        search_k: Union[None, Unset, int]
        if isinstance(self.search_k, Unset):
            search_k = UNSET
        else:
            search_k = self.search_k

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nprobe": nprobe,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if ef is not UNSET:
            field_dict["ef"] = ef
        if search_k is not UNSET:
            field_dict["search_k"] = search_k

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nprobe = d.pop("nprobe")

        object_type = d.pop("object_type", UNSET)

        def _parse_ef(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ef = _parse_ef(d.pop("ef", UNSET))

        def _parse_search_k(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        search_k = _parse_search_k(d.pop("search_k", UNSET))

        query_meta_params = cls(
            nprobe=nprobe,
            object_type=object_type,
            ef=ef,
            search_k=search_k,
        )

        query_meta_params.additional_properties = d
        return query_meta_params

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
