"Parsing for date / time ranges."

import re

from pydantic import BaseModel

_range_pattern = re.compile(r"(\d+)([YMWDHS])")


class TimeRange(BaseModel):
    year: int = 0
    month: int = 0
    week: int = 0
    day: int = 0
    hour: int = 0
    minute: int = 0
    second: int = 0

    @staticmethod
    def parse(input_string: str) -> "TimeRange":
        text = input_string.strip()
        if text[0] != "P":
            raise ValueError("Duration must start with a P")
        text = text[1:]

        parts = text.split("T")

        if len(parts) > 2:
            raise ValueError(f"More than 1 time delimiter present in: {input_string}")

        date = parts[0]
        time = parts[1] if len(parts) == 2 else ""

        date_map = {"Y": "year", "M": "month", "W": "week", "D": "day"}
        time_map = {"H": "hour", "M": "minute", "S": "second"}

        args = {
            **TimeRange.extract(date, date_map),
            **TimeRange.extract(time, time_map),
        }

        if not args:
            raise ValueError(f"No duration components in {input_string}")

        return TimeRange(**args)

    @staticmethod
    def extract(section: str, mapping: dict[str, str]) -> dict[str, int]:
        found = _range_pattern.findall(section)

        consumed = "".join(time + lookup for time, lookup in found)
        if consumed != section:
            raise ValueError(f"Invalid duration component in {section!r}")

        result: dict[str, int] = {}
        for quantity, letter in found:
            if letter not in mapping:
                raise ValueError(f"Unexpected component '{letter}' in {section!r}")
            result[mapping[letter]] = int(quantity)

        return result

    def duration_string(self) -> str:
        date_component = [
            (self.year, "Y"),
            (self.month, "M"),
            (self.week, "W"),
            (self.day, "D"),
        ]
        date_component = "".join([f"{p[0]}{p[1]}" for p in date_component if p[0] > 0])

        time_component = [
            (self.hour, "H"),
            (self.minute, "M"),
            (self.second, "S"),
        ]
        time_component = "".join([f"{p[0]}{p[1]}" for p in time_component if p[0] > 0])
        if time_component:
            time_component = "T" + time_component

        return "P" + "".join([date_component, time_component])

    def pretty_print(self) -> str:
        parts = [
            (self.year, "year"),
            (self.month, "month"),
            (self.week, "week"),
            (self.day, "day"),
            (self.hour, "hour"),
            (self.minute, "minute"),
            (self.second, "second"),
        ]
        return ", ".join(
            f"{n} {label}" if n == 1 else f"{n} {label}s" for n, label in parts if n > 0
        )
