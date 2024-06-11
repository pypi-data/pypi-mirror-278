from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hit import Hit


T = TypeVar("T", bound="QueryResponse")


@_attrs_define
class QueryResponse:
    """
    Attributes:
        collection_name (str):
        hits (List[List['Hit']]):
        query_latency (float):
        total_latency (float):
        object_type (Union[Literal['QueryResponse'], Unset]):  Default: 'QueryResponse'.
    """

    collection_name: str
    hits: List[List["Hit"]]
    query_latency: float
    total_latency: float
    object_type: Union[Literal["QueryResponse"], Unset] = "QueryResponse"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name

        hits = []
        for hits_item_data in self.hits:
            hits_item = []
            for hits_item_item_data in hits_item_data:
                hits_item_item = hits_item_item_data.to_dict()
                hits_item.append(hits_item_item)

            hits.append(hits_item)

        query_latency = self.query_latency

        total_latency = self.total_latency

        object_type = self.object_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "hits": hits,
                "query_latency": query_latency,
                "total_latency": total_latency,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.hit import Hit

        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = []
            _hits_item = hits_item_data
            for hits_item_item_data in _hits_item:
                hits_item_item = Hit.from_dict(hits_item_item_data)

                hits_item.append(hits_item_item)

            hits.append(hits_item)

        query_latency = d.pop("query_latency")

        total_latency = d.pop("total_latency")

        object_type = d.pop("object_type", UNSET)

        query_response = cls(
            collection_name=collection_name,
            hits=hits,
            query_latency=query_latency,
            total_latency=total_latency,
            object_type=object_type,
        )

        query_response.additional_properties = d
        return query_response

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
