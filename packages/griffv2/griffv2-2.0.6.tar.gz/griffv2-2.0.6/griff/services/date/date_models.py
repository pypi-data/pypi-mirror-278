import copy
import datetime
from typing import Any, Union

import arrow
from arrow import Arrow

DateTimeIn = Union[str, datetime.datetime, datetime.date, int, float, Arrow]


class DateTime:
    def __init__(self, datetime: DateTimeIn):
        self._value = (
            datetime if isinstance(datetime, Arrow) else self._check_is_valid(datetime)
        )
        self._timezone = "UTC"

    def to_mysql_date(self) -> str:
        return self._format("YYYY-MM-DD")

    def to_mysql_datetime(self) -> str:
        return self._format("YYYY-MM-DD HH:mm:ss.SSSSSS")

    def to_date(self) -> datetime.date:
        return self._value.date()

    def to_datetime(self) -> datetime.datetime:
        return self._value.to(self._timezone).datetime

    def to_timestamp(self) -> float:
        return self._value.timestamp()

    def copy(self):
        return copy.copy(self)

    def format(self, format: str):
        return self._format(format)

    @classmethod
    def _check_is_valid(cls, value: Any) -> Arrow:
        try:
            return arrow.get(value)
        except (TypeError, arrow.parser.ParserError) as e:
            raise ValueError(str(e))

    def __copy__(self):
        return DateTime(self._value)

    def __repr__(self):
        return self._value.format("YYYY-MM-DDTHH:mm:ss.SSSSSSZZ")

    def __eq__(self, other):
        return self._value == other._value

    def __ne__(self, other):
        return self._value != other._value

    def __ge__(self, other):
        return self._value >= other._value

    def __le__(self, other):
        return self._value <= other._value

    def __gt__(self, other):
        return self._value > other._value

    def __lt__(self, other):
        return self._value < other._value

    def _format(self, date_format) -> str:
        return self._value.to(self._timezone).format(date_format)


class Date(DateTime):
    def __init__(self, datetime: DateTimeIn):
        super().__init__(datetime)
        self._value = arrow.get(self._value.date())

    def __copy__(self):
        return Date(self._value)

    def __repr__(self):
        return self._value.format("YYYY-MM-DD")  # pragma: no cover
