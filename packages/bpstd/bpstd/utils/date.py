import datetime
import time


def time_to_date(time_at):
    """convert time to date-str
    :param time_at: datetime.datetime(2017, 8, 23, 15, 40, 32, 927512)
    :return: 2017-08-23
    """
    fmt = "%Y-%m-%d"
    if not isinstance(time_at, datetime.datetime):
        time_at = datetime.datetime.today()
    date_at = time_at.strftime(fmt)
    return date_at


def date_to_duration(start_at="2017-9-11", after_days=1):
    """default: [2017-09-11 00:00:00, 2017-09-12 00:00:00]

    :param start_at: str
    :param after_days: a day
    :return: []
    """
    fmt = "%Y-%m-%d"
    if not isinstance(after_days, int):
        return (None, None)
    if isinstance(start_at, datetime.datetime):
        start_at = time_to_date(start_at)

    start = datetime.datetime.strptime(start_at, fmt)
    duration = datetime.timedelta(days=after_days)
    end = start + duration
    return start, end


def time_duration_before_hours(input_time=None, hours=3):
    """时间段: [输入时间, 提前几个小时的时间段]

    :param input_time:
    :param hours:
    :return:
    """
    if not input_time:
        input_time = datetime.datetime.now()
    start_at = input_time - datetime.timedelta(hours=hours)
    return start_at, input_time


def time_duration_before_input_date(input_date=None, before_days=1):
    """时间段: [输入日期, 提前 N 天的时间段]

    :param input_date: type(datetime.date)
    :param before_days: N, type(int)
    :return: (datetime.datetime(2017, 10, 19, 0, 0), datetime.datetime(2017, 10, 20, 0, 0))
    """
    fmt = "%Y-%m-%d"

    if not input_date:
        input_date = datetime.date.today()
    elif not isinstance(input_date, (datetime.date, datetime.datetime)):
        raise TypeError("Invalid Date Format")
    if isinstance(input_date, datetime.datetime):
        input_date = input_date.date()

    start = input_date - datetime.timedelta(days=before_days)

    start_at = datetime.datetime.strptime(str(start), fmt)
    end_at = datetime.datetime.strptime(str(input_date), fmt)
    return start_at, end_at


def unix_to_datetime(input_unix=None, format=None):
    return datetime.datetime.fromtimestamp(
        int(input_unix),
    ).strftime(format)


def utc_now_str(timedelta_day=None):
    if timedelta_day == None:
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return (
            datetime.datetime.utcnow() - datetime.timedelta(days=timedelta_day)
        ).strftime("%Y-%m-%d %H:%M:%S")


def utc_now_unixtimestamp():
    n = datetime.datetime.utcnow()
    unix_time = int(time.mktime(n.timetuple()))
    return str(unix_time)


if __name__ == "__main__":
    t = datetime.datetime.now()
    t2d = time_to_date(t)
    d_start, d_end = date_to_duration(t2d)
    d2_start, d2_end = date_to_duration(t)
    print("t: ", t)
    print("t to date:", t2d)
    print("start:", d_start, "end:", d_end)
    print("start2:", d_start, "end2:", d_end)
    print("v:", time_duration_before_input_date())
    print(utc_now_str())
