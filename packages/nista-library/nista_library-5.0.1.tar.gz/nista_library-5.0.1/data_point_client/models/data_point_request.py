from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.en_data_point_existence_dto import EnDataPointExistenceDTO
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_point_info import DataPointInfo
    from ..models.data_point_origin import DataPointOrigin


T = TypeVar("T", bound="DataPointRequest")


@attr.s(auto_attribs=True)
class DataPointRequest:
    """
    Attributes:
        name (Union[Unset, None, str]):
        description (Union[Unset, None, str]):
        data_point_info (Union[Unset, None, DataPointInfo]):
        facility_id (Union[Unset, None, str]):
        existence (Union[Unset, None, EnDataPointExistenceDTO]):
        tags (Union[Unset, None, List[str]]):
        origin (Union[Unset, None, DataPointOrigin]):
    """

    name: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    data_point_info: Union[Unset, None, "DataPointInfo"] = UNSET
    facility_id: Union[Unset, None, str] = UNSET
    existence: Union[Unset, None, EnDataPointExistenceDTO] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    origin: Union[Unset, None, "DataPointOrigin"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        data_point_info: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.data_point_info, Unset):
            data_point_info = self.data_point_info.to_dict() if self.data_point_info else None

        facility_id = self.facility_id
        existence: Union[Unset, None, str] = UNSET
        if not isinstance(self.existence, Unset):
            existence = self.existence.value if self.existence else None

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        origin: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.origin, Unset):
            origin = self.origin.to_dict() if self.origin else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if data_point_info is not UNSET:
            field_dict["dataPointInfo"] = data_point_info
        if facility_id is not UNSET:
            field_dict["facilityId"] = facility_id
        if existence is not UNSET:
            field_dict["existence"] = existence
        if tags is not UNSET:
            field_dict["tags"] = tags
        if origin is not UNSET:
            field_dict["origin"] = origin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_point_info import DataPointInfo
        from ..models.data_point_origin import DataPointOrigin

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _data_point_info = d.pop("dataPointInfo", UNSET)
        data_point_info: Union[Unset, None, DataPointInfo]
        if _data_point_info is None:
            data_point_info = None
        elif isinstance(_data_point_info, Unset):
            data_point_info = UNSET
        else:
            data_point_info = DataPointInfo.from_dict(_data_point_info)

        facility_id = d.pop("facilityId", UNSET)

        _existence = d.pop("existence", UNSET)
        existence: Union[Unset, None, EnDataPointExistenceDTO]
        if _existence is None:
            existence = None
        elif isinstance(_existence, Unset):
            existence = UNSET
        else:
            existence = EnDataPointExistenceDTO(_existence)

        tags = cast(List[str], d.pop("tags", UNSET))

        _origin = d.pop("origin", UNSET)
        origin: Union[Unset, None, DataPointOrigin]
        if _origin is None:
            origin = None
        elif isinstance(_origin, Unset):
            origin = UNSET
        else:
            origin = DataPointOrigin.from_dict(_origin)

        data_point_request = cls(
            name=name,
            description=description,
            data_point_info=data_point_info,
            facility_id=facility_id,
            existence=existence,
            tags=tags,
            origin=origin,
        )

        return data_point_request
