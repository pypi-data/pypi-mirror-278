from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.date_range_dto import DateRangeDTO


T = TypeVar("T", bound="FinishExecutionResultDataRequest")


@attr.s(auto_attribs=True)
class FinishExecutionResultDataRequest:
    """
    Attributes:
        unit (Union[Unset, None, str]):
        time_zone (Union[Unset, None, str]):
        is_major_change (Union[Unset, bool]):
        sub_series (Union[Unset, None, List['DateRangeDTO']]):
    """

    unit: Union[Unset, None, str] = UNSET
    time_zone: Union[Unset, None, str] = UNSET
    is_major_change: Union[Unset, bool] = UNSET
    sub_series: Union[Unset, None, List["DateRangeDTO"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        unit = self.unit
        time_zone = self.time_zone
        is_major_change = self.is_major_change
        sub_series: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sub_series, Unset):
            if self.sub_series is None:
                sub_series = None
            else:
                sub_series = []
                for sub_series_item_data in self.sub_series:
                    sub_series_item = sub_series_item_data.to_dict()

                    sub_series.append(sub_series_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if unit is not UNSET:
            field_dict["unit"] = unit
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if is_major_change is not UNSET:
            field_dict["isMajorChange"] = is_major_change
        if sub_series is not UNSET:
            field_dict["subSeries"] = sub_series

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.date_range_dto import DateRangeDTO

        d = src_dict.copy()
        unit = d.pop("unit", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        is_major_change = d.pop("isMajorChange", UNSET)

        sub_series = []
        _sub_series = d.pop("subSeries", UNSET)
        for sub_series_item_data in _sub_series or []:
            sub_series_item = DateRangeDTO.from_dict(sub_series_item_data)

            sub_series.append(sub_series_item)

        finish_execution_result_data_request = cls(
            unit=unit,
            time_zone=time_zone,
            is_major_change=is_major_change,
            sub_series=sub_series,
        )

        return finish_execution_result_data_request
