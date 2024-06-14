import datetime
import time


class DateUtil:

    @staticmethod
    def get_time_stamp():
        """获取当前时间戳 13位"""
        return int(round(time.time() * 1000))

    @staticmethod
    def timestamp_to_format(timestamp: int, format_str="%m/%d/%Y"):
        pst_timezone = datetime.timezone(datetime.timedelta(hours=-8))
        dt = datetime.datetime.fromtimestamp(timestamp / 1000, pst_timezone)
        formatted_time = dt.strftime(format_str)
        return formatted_time