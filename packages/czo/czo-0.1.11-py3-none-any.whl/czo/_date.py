import datetime
import time


class DateLib:
    """
    提供了一组静态方法，用于处理日期和时间的常见操作。
    """

    @staticmethod
    def timestamp() -> int:
        """
        返回当前时间的时间戳。
        """
        return int(time.time())

    @staticmethod
    def timestamp_ms() -> int:
        """
        返回当前时间的时间戳。
        """
        return int(time.time() * 1000)

    @staticmethod
    def now_date() -> str:
        """
        返回当前日期和时间的格式化字符串。

        Returns:
            当前日期和时间的格式化字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> now_date()
            '2022-01-01 12:00:00'
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def now_ymd() -> list:
        """
        返回当前日期的年、月、日。

        Returns:
            包含当前年、月、日的列表。

        Examples:
            >>> now_ymd()
            ['2022', '01', '01']
        """
        now_date = datetime.datetime.now()
        y = str(now_date.year)
        m = str(now_date.month)
        d = str(now_date.day)
        return [y, m, d]

    @staticmethod
    def timestamp_to_date(timestamp) -> str:
        """
        将时间戳转换为日期字符串。

        Args:
            timestamp: 要转换的时间戳。

        Returns:
            转换后的日期字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> timestamp_to_date(1640995200)
            '2022-01-01 12:00:00'
            >>> timestamp_to_date(1640995200000)
            '2022-01-01 12:00:00'
        """
        if len(str(timestamp)) == 13:
            timestamp = int(timestamp) / 1000.0
        struct_time = time.localtime(int(timestamp))
        return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)

    @staticmethod
    def date_to_timestamp(date, ms=False) -> int:
        """
        将日期转换为时间戳。

        Args:
            date: 要转换的日期，格式为"%Y-%m-%d %H:%M:%S"。
            ms: 是否返回毫秒级时间戳，默认为False。

        Returns:
            转换后的时间戳，单位为秒或毫秒，取决于ms参数的值。

        Examples:
            >>> date_to_timestamp("2022-01-01 12:00:00")
            1640995200
            >>> date_to_timestamp("2022-01-01 12:00:00", ms=True)
            1640995200000
        """
        struct_time = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        if ms:
            return int(time.mktime(struct_time)) * 1000
        return int(time.mktime(struct_time))

    @staticmethod
    def yesterday_zero_point_timestamp(day=1, ms=False) -> int:
        """
        返回昨天零点的时间戳。

        Args:
            day: 要减去的天数，默认为1。
            ms: 是否返回毫秒级时间戳，默认为False。

        Returns:
            昨天零点的时间戳，单位为秒或毫秒，取决于ms参数的值。

        Examples:
            >>> yesterday_zero_point_timestamp()
            1640995200
            >>> yesterday_zero_point_timestamp(day=2, ms=True)
            1640908800000
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=day)
        if ms:
            return int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d'))) * 1000
        return int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))

    @staticmethod
    def difference_time_two(date1: str, date2: str, reversal: bool = False) -> float:
        """
        计算两个日期之间的时间差（以秒为单位）。

        Args:
            date1: 第一个日期，格式为"%Y-%m-%d %H:%M:%S"。
            date2: 第二个日期，格式为"%Y-%m-%d %H:%M:%S"。
            reversal: 默认使用 date2 - date1 的方式计算时间差，如果为 True，则使用 date1 - date2 的方式计算时间差。

        Returns:
            两个日期之间的时间差，以秒为单位。

        Examples:
            >>> difference_time_two("2022-01-01 10:00:00", "2022-01-01 12:00:00")
            7200.0
        """
        date1 = datetime.datetime.strptime(date1.strip(), "%Y-%m-%d %H:%M:%S")
        date2 = datetime.datetime.strptime(date2.strip(), "%Y-%m-%d %H:%M:%S")
        if reversal:
            date1, date2 = date2, date1
        return (date2 - date1).total_seconds()

    @staticmethod
    def date_before_minutes(value) -> str:
        """
        返回指定分钟数之前的日期和时间。

        Args:
            value: 要减去的分钟数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_minutes(30)
            '2022-01-01 11:30:00'
        """
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(minutes=int(value))
        return now_time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def date_before_hours(value) -> str:
        """
        返回指定小时数之前的日期和时间。

        Args:
            value: 要减去的小时数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_hours(3)
            '2022-01-01 09:00:00'
        """
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(hours=int(value))
        return now_time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def date_before_days(day: int) -> str:
        """
        返回指定天数之前的日期和时间。

        Args:
            day: 要减去的天数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_days(7)
            '2022-01-01 12:00:00'
        """
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=-day)
        return (today + offset).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def time_handler(date_str: str) -> str:
        """
        将格式为"%Y-%m-%dT%H:%M:%S.%fZ"的日期字符串转换为格式化的本地时间字符串。

        Args:
            date_str: 要转换的日期字符串。

        Returns:
            格式化的本地时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> time_handler("2022-01-01T12:00:00.000Z")
            '2022-01-01 20:00:00'
        """
        date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        local_time = date + datetime.timedelta(hours=8)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def http_header_time_to_str(date_str: str):
        """
        将HTTP头时间字符串转换为格式化的日期和时间字符串。

        Args:
            date_str: 要转换的HTTP头时间字符串。

        Returns:
            格式化的日期和时间字符串，格式为"YYYY-MM-DD HH:MM:SS"。

        Examples:
            >>> http_header_time_to_str("Sat, 01 Jan 2022 12:00:00 GMT")
            '2022-01-01 20:00:00'
        """
        # 解析字符串为 datetime 对象
        parsed_date = datetime.datetime.strptime(
            date_str, "%a, %d %b %Y %H:%M:%S %Z")
        parsed_date = parsed_date + datetime.timedelta(hours=8)
        # 格式化为想要的时间格式
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def now_start_end(timestamp: bool = False) -> tuple:
        """
        返回当前日期的开始和结束时间。

        Args:
            timestamp (bool, 可选): 如果为True，则返回开始和结束时间的时间戳。默认为False。

        Returns:
            tuple: 包含当前日期的开始时间（00:00:00）和结束时间（23:59:59）的元组。如果timestamp为True，则返回开始和结束时间的时间戳。
        """
        # 获取当前日期时间
        now = datetime.datetime.now()
        # 获取当天开始时间（即 00:00:00）
        start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        # 获取当天结束时间（即 23:59:59）
        end_of_day = datetime.datetime(
            now.year, now.month, now.day, 23, 59, 59)
        if timestamp:
            return int(start_of_day.timestamp()), int(end_of_day.timestamp())
        return str(start_of_day), str(end_of_day)

    @staticmethod
    def fmt_date(fmt="%Y-%m-%d %H:%M:%S") -> str:
        """格式化当前时间。方便创建不同的字面量。

        Args:
            fmt (str): 格式. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            str: 当前时间格式化后的时间字符串

        Examples:
            >>> fmt_date()
            "2024-05-13 14:58:18"
        """
        return time.strftime(fmt, time.localtime(int(time.time())))
