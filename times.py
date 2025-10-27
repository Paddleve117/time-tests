import datetime


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        start1_dt = datetime.datetime.strptime(start1, "%Y-%m-%d %H:%M:%S")
        end1_dt = datetime.datetime.strptime(end1, "%Y-%m-%d %H:%M:%S")
        for start2, end2 in range2:
            start2_dt = datetime.datetime.strptime(start2, "%Y-%m-%d %H:%M:%S")
            end2_dt = datetime.datetime.strptime(end2, "%Y-%m-%d %H:%M:%S")
            low_dt = max(start1_dt, start2_dt)
            high_dt = min(end1_dt, end2_dt)
            # only include positive-length overlaps (exclude touching endpoints)
            if low_dt < high_dt:
                overlap_time.append((low_dt.strftime("%Y-%m-%d %H:%M:%S"),
                                     high_dt.strftime("%Y-%m-%d %H:%M:%S")))
    return overlap_time