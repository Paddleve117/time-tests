from times import compute_overlap_time, time_range
import pytest
import yaml
from pathlib import Path

_fixture_path = Path(__file__).with_name("fixture.yaml")
_data = yaml.safe_load(_fixture_path.read_text())

_params = []
for case in _data:
    info = list(case.values())[0]  # 每个列表项是 {name: { ... }}
    def build(tr):
        # tr 是字典，包含 start, end，可选 number_of_intervals 和 gap_between_intervals_s
        start = tr["start"]
        end = tr["end"]
        n = tr.get("number_of_intervals", 1)
        gap = tr.get("gap_between_intervals_s", 0)
        return time_range(start, end, n, gap)
    r1 = build(info["time_range_1"])
    r2 = build(info["time_range_2"])
    expected = [tuple(x) for x in info.get("expected", [])]
    _params.append((r1, r2, expected))

@pytest.mark.parametrize("range1, range2, expected", _params)
def test_overlap_param(range1, range2, expected):
    assert compute_overlap_time(range1, range2) == expected

# def test_generic_case():
#     large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
#     short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
#     expected = [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
#     assert compute_overlap_time(large, short) == expected

# def test_no_overlap(): # 两个不重叠的时间范围
#     a = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 1)
#     b = time_range("2020-01-01 12:00:00", "2020-01-01 13:00:00", 1)
#     assert compute_overlap_time(a, b) == []

# def test_multiple_intervals(): # 多个时间范围的重叠
#     a = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 3, 0)
#     b = time_range("2020-01-01 10:10:00", "2020-01-01 10:50:00", 2, 0)
#     expected = [
#         ("2020-01-01 10:10:00", "2020-01-01 10:20:00"),
#         ("2020-01-01 10:20:00", "2020-01-01 10:30:00"),
#         ("2020-01-01 10:30:00", "2020-01-01 10:40:00"),
#         ("2020-01-01 10:40:00", "2020-01-01 10:50:00"),
#     ]
#     assert compute_overlap_time(a, b) == expected

# def test_touching_intervals_no_overlap(): # 边界接触但不重叠的时间范围
#     a = time_range("2021-06-01 10:00:00", "2021-06-01 10:30:00", 1)
#     b = time_range("2021-06-01 10:30:00", "2021-06-01 11:00:00", 1)
#     # touching at 10:30:00 -> should be considered no overlap (zero-length)
#     assert compute_overlap_time(a, b) == []

# @pytest.mark.parametrize("range1, range2, expected", [
#     (
#         time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
#         time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
#         [("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
#          ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
#     ),
#     (
#         time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 1),
#         time_range("2020-01-01 12:00:00", "2020-01-01 13:00:00", 1),
#         []
#     ),
#     (
#         time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 3, 0),
#         time_range("2020-01-01 10:10:00", "2020-01-01 10:50:00", 2, 0),
#         [
#             ("2020-01-01 10:10:00", "2020-01-01 10:20:00"),
#             ("2020-01-01 10:20:00", "2020-01-01 10:30:00"),
#             ("2020-01-01 10:30:00", "2020-01-01 10:40:00"),
#             ("2020-01-01 10:40:00", "2020-01-01 10:50:00"),
#         ]
#     ),
#     (
#         time_range("2021-06-01 10:00:00", "2021-06-01 10:30:00", 1),
#         time_range("2021-06-01 10:30:00", "2021-06-01 11:00:00", 1),
#         []
#     ),
# ])
# def test_overlap_param(range1, range2, expected):
#     assert compute_overlap_time(range1, range2) == expected

def test_time_range_backwards(): # 测试时间范围反向
    # end_time earlier than start_time should raise ValueError
    with pytest.raises(ValueError) as exc:
        time_range("2020-01-02 10:00:00", "2020-01-01 10:00:00", 1)
    assert "before start_time" in str(exc.value)