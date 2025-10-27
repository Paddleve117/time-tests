from times import compute_overlap_time, time_range

def test_generic_case():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
    assert compute_overlap_time(large, short) == expected

def test_no_overlap(): # 两个不重叠的时间范围
    a = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 1)
    b = time_range("2020-01-01 12:00:00", "2020-01-01 13:00:00", 1)
    assert compute_overlap_time(a, b) == []

def test_multiple_intervals(): # 多个时间范围的重叠
    a = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 3, 0)
    b = time_range("2020-01-01 10:10:00", "2020-01-01 10:50:00", 2, 0)
    expected = [
        ("2020-01-01 10:10:00", "2020-01-01 10:20:00"),
        ("2020-01-01 10:20:00", "2020-01-01 10:30:00"),
        ("2020-01-01 10:30:00", "2020-01-01 10:40:00"),
        ("2020-01-01 10:40:00", "2020-01-01 10:50:00"),
    ]
    assert compute_overlap_time(a, b) == expected

def test_touching_intervals_no_overlap(): # 边界接触但不重叠的时间范围
    a = time_range("2021-06-01 10:00:00", "2021-06-01 10:30:00", 1)
    b = time_range("2021-06-01 10:30:00", "2021-06-01 11:00:00", 1)
    # touching at 10:30:00 -> should be considered no overlap (zero-length)
    assert compute_overlap_time(a, b) == []