from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.en_import_options import EnImportOptions
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sub_series_request import SubSeriesRequest


T = TypeVar("T", bound="AppendTimeSeriesRequest")


@attr.s(auto_attribs=True)
class AppendTimeSeriesRequest:
    """
    Attributes:
        sub_series (List['SubSeriesRequest']):
        unit (Union[Unset, None, str]):
        import_options (Union[Unset, EnImportOptions]):
        block_to_right (Union[Unset, bool]):
        time_zone (Union[Unset, None, str]):
    """

    sub_series: List["SubSeriesRequest"]
    unit: Union[Unset, None, str] = UNSET
    import_options: Union[Unset, EnImportOptions] = UNSET
    block_to_right: Union[Unset, bool] = UNSET
    time_zone: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sub_series = []
        for sub_series_item_data in self.sub_series:
            sub_series_item = sub_series_item_data.to_dict()

            sub_series.append(sub_series_item)

        unit = self.unit
        import_options: Union[Unset, str] = UNSET
        if not isinstance(self.import_options, Unset):
            import_options = self.import_options.value

        block_to_right = self.block_to_right
        time_zone = self.time_zone

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "subSeries": sub_series,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if import_options is not UNSET:
            field_dict["importOptions"] = import_options
        if block_to_right is not UNSET:
            field_dict["blockToRight"] = block_to_right
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sub_series_request import SubSeriesRequest

        d = src_dict.copy()
        sub_series = []
        _sub_series = d.pop("subSeries")
        for sub_series_item_data in _sub_series:
            sub_series_item = SubSeriesRequest.from_dict(sub_series_item_data)

            sub_series.append(sub_series_item)

        unit = d.pop("unit", UNSET)

        _import_options = d.pop("importOptions", UNSET)
        import_options: Union[Unset, EnImportOptions]
        if isinstance(_import_options, Unset):
            import_options = UNSET
        else:
            import_options = EnImportOptions(_import_options)

        block_to_right = d.pop("blockToRight", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        append_time_series_request = cls(
            sub_series=sub_series,
            unit=unit,
            import_options=import_options,
            block_to_right=block_to_right,
            time_zone=time_zone,
        )

        return append_time_series_request
