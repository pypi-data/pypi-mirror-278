from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.collection_schema import CollectionSchema


T = TypeVar("T", bound="Collection")


@_attrs_define
class Collection:
    """
    Attributes:
        name (str):
        coll_schema (CollectionSchema):
        object_type (Union[Literal['Collection'], Unset]):  Default: 'Collection'.
        consistency_level (Union[Unset, str]):  Default: 'Session'.
        approx (Union[None, Unset, bool]):  Default: True.
    """

    name: str
    coll_schema: "CollectionSchema"
    object_type: Union[Literal["Collection"], Unset] = "Collection"
    consistency_level: Union[Unset, str] = "Session"
    approx: Union[None, Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        coll_schema = self.coll_schema.to_dict()

        object_type = self.object_type

        consistency_level = self.consistency_level

        approx: Union[None, Unset, bool]
        if isinstance(self.approx, Unset):
            approx = UNSET
        else:
            approx = self.approx

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "coll_schema": coll_schema,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if consistency_level is not UNSET:
            field_dict["consistency_level"] = consistency_level
        if approx is not UNSET:
            field_dict["approx"] = approx

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.collection_schema import CollectionSchema

        d = src_dict.copy()
        name = d.pop("name")

        coll_schema = CollectionSchema.from_dict(d.pop("coll_schema"))

        object_type = d.pop("object_type", UNSET)

        consistency_level = d.pop("consistency_level", UNSET)

        def _parse_approx(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        approx = _parse_approx(d.pop("approx", UNSET))

        collection = cls(
            name=name,
            coll_schema=coll_schema,
            object_type=object_type,
            consistency_level=consistency_level,
            approx=approx,
        )

        collection.additional_properties = d
        return collection

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
