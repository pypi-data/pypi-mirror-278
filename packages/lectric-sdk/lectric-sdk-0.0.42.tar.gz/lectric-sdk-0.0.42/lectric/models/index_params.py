from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexParams")


@_attrs_define
class IndexParams:
    """
    Attributes:
        object_type (Union[Literal['IndexParams'], Unset]):  Default: 'IndexParams'.
        nlist (Union[None, Unset, int]): Number of cluster units Default: 128.
        quant (Union[None, Unset, int]): Number of factors of product quantization
        nbits (Union[None, Unset, int]): Number of bits in which each low-dimensional vector is stored
        m (Union[None, Unset, int]): Maximum degree of the node
        ef_construction (Union[None, Unset, int]): Search scope
        pqm (Union[None, Unset, int]): Number of factors of product quantization
        ntrees (Union[None, Unset, int]): The number of methods of space division
    """

    object_type: Union[Literal["IndexParams"], Unset] = "IndexParams"
    nlist: Union[None, Unset, int] = 128
    quant: Union[None, Unset, int] = UNSET
    nbits: Union[None, Unset, int] = UNSET
    m: Union[None, Unset, int] = UNSET
    ef_construction: Union[None, Unset, int] = UNSET
    pqm: Union[None, Unset, int] = UNSET
    ntrees: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_type = self.object_type

        nlist: Union[None, Unset, int]
        if isinstance(self.nlist, Unset):
            nlist = UNSET
        else:
            nlist = self.nlist

        quant: Union[None, Unset, int]
        if isinstance(self.quant, Unset):
            quant = UNSET
        else:
            quant = self.quant

        nbits: Union[None, Unset, int]
        if isinstance(self.nbits, Unset):
            nbits = UNSET
        else:
            nbits = self.nbits

        m: Union[None, Unset, int]
        if isinstance(self.m, Unset):
            m = UNSET
        else:
            m = self.m

        ef_construction: Union[None, Unset, int]
        if isinstance(self.ef_construction, Unset):
            ef_construction = UNSET
        else:
            ef_construction = self.ef_construction

        pqm: Union[None, Unset, int]
        if isinstance(self.pqm, Unset):
            pqm = UNSET
        else:
            pqm = self.pqm

        ntrees: Union[None, Unset, int]
        if isinstance(self.ntrees, Unset):
            ntrees = UNSET
        else:
            ntrees = self.ntrees

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if nlist is not UNSET:
            field_dict["nlist"] = nlist
        if quant is not UNSET:
            field_dict["quant"] = quant
        if nbits is not UNSET:
            field_dict["nbits"] = nbits
        if m is not UNSET:
            field_dict["M"] = m
        if ef_construction is not UNSET:
            field_dict["efConstruction"] = ef_construction
        if pqm is not UNSET:
            field_dict["PQM"] = pqm
        if ntrees is not UNSET:
            field_dict["ntrees"] = ntrees

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_type = d.pop("object_type", UNSET)

        def _parse_nlist(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        nlist = _parse_nlist(d.pop("nlist", UNSET))

        def _parse_quant(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        quant = _parse_quant(d.pop("quant", UNSET))

        def _parse_nbits(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        nbits = _parse_nbits(d.pop("nbits", UNSET))

        def _parse_m(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        m = _parse_m(d.pop("M", UNSET))

        def _parse_ef_construction(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ef_construction = _parse_ef_construction(d.pop("efConstruction", UNSET))

        def _parse_pqm(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pqm = _parse_pqm(d.pop("PQM", UNSET))

        def _parse_ntrees(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ntrees = _parse_ntrees(d.pop("ntrees", UNSET))

        index_params = cls(
            object_type=object_type,
            nlist=nlist,
            quant=quant,
            nbits=nbits,
            m=m,
            ef_construction=ef_construction,
            pqm=pqm,
            ntrees=ntrees,
        )

        index_params.additional_properties = d
        return index_params

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
