import pytest

from housekeeping.models.time_range import TimeRange


class TestTimeRange:
    @pytest.mark.parametrize(
        "range_string,components",
        [
            ("P1M", {"month": 1}),
            ("PT1M", {"minute": 1}),
            ("PT1H2M", {"hour": 1, "minute": 2}),
            ("P1MT5M", {"month": 1, "minute": 5}),
            (
                "P3Y6M7W4DT12H30M5S",
                {
                    "year": 3,
                    "month": 6,
                    "week": 7,
                    "day": 4,
                    "hour": 12,
                    "minute": 30,
                    "second": 5,
                },
            ),
        ],
    )
    def test_parse_success(self, range_string: str, components: dict[str, int]):
        assert TimeRange.parse(range_string) == TimeRange(**components)
        assert TimeRange.parse(range_string).duration_string() == range_string
