from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_params import QueryParams


T = TypeVar("T", bound="VectorQuerySpec")


@_attrs_define
class VectorQuerySpec:
    """
    Attributes:
        data (List[List[Any]]):
        collection_name (str):
        search_field (str):
        search_params (QueryParams):
        output_fields (List[str]):
        limit (int):
        object_type (Union[Literal['VectorQuerySpec'], Unset]):  Default: 'VectorQuerySpec'.
        expr (Union[None, Unset, str]):
    """

    data: List[List[Any]]
    collection_name: str
    search_field: str
    search_params: "QueryParams"
    output_fields: List[str]
    limit: int
    object_type: Union[Literal["VectorQuerySpec"], Unset] = "VectorQuerySpec"
    expr: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data

            data.append(data_item)

        collection_name = self.collection_name

        search_field = self.search_field

        search_params = self.search_params.to_dict()

        output_fields = self.output_fields

        limit = self.limit

        object_type = self.object_type

        expr: Union[None, Unset, str]
        if isinstance(self.expr, Unset):
            expr = UNSET
        else:
            expr = self.expr

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "collection_name": collection_name,
                "search_field": search_field,
                "search_params": search_params,
                "output_fields": output_fields,
                "limit": limit,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if expr is not UNSET:
            field_dict["expr"] = expr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query_params import QueryParams

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = cast(List[Any], data_item_data)

            data.append(data_item)

        collection_name = d.pop("collection_name")

        search_field = d.pop("search_field")

        search_params = QueryParams.from_dict(d.pop("search_params"))

        output_fields = cast(List[str], d.pop("output_fields"))

        limit = d.pop("limit")

        object_type = d.pop("object_type", UNSET)

        def _parse_expr(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expr = _parse_expr(d.pop("expr", UNSET))

        vector_query_spec = cls(
            data=data,
            collection_name=collection_name,
            search_field=search_field,
            search_params=search_params,
            output_fields=output_fields,
            limit=limit,
            object_type=object_type,
            expr=expr,
        )

        vector_query_spec.additional_properties = d
        return vector_query_spec

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
