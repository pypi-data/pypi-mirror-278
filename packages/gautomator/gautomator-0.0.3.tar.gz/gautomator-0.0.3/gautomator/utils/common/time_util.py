import time
from datetime import datetime, timezone, timedelta
import calendar

from ...const.common import TimeConst
from .logger_util import logger


class TimeUtil:

    @staticmethod
    def convert_unix_to_timestamp(ts):
        """ convert unix timestamp to local readable time format YYYY-MM-DD (covered timezone)"""
        utc_time = datetime.fromtimestamp(int(ts), timezone.utc)
        local_time = utc_time.astimezone()
        return local_time.strftime('%Y-%m-%d')

    @staticmethod
    def sleep(duration: float):
        logger.debug('------- Sleep %s second to sync data' % duration)
        time.sleep(duration)

    @staticmethod
    def long_sleep():
        TimeUtil.sleep(30)

    @staticmethod
    def short_sleep(sleep_tm: int = 3):
        TimeUtil.sleep(sleep_tm)

    @staticmethod
    def delay_time():
        TimeUtil.sleep(0.1)

    @staticmethod
    def get_current_date_time(datetime_format: str = TimeConst.Format.FORMAT_DD_MM_YY):
        return datetime.fromtimestamp(time.time()).strftime(datetime_format)

    @staticmethod
    def get_current_date_time_by_new_format(dt_format: str = TimeConst.Format.FORMAT_DD_MM_YY, new_format: str = TimeConst.Format.FORMAT_DD_MM_YY):
        cur_time = datetime.fromtimestamp(time.time()).strftime(dt_format)
        return TimeUtil.convert_date_time_by_format(cur_time, new_format)

    @staticmethod
    def convert_date_time_by_format(time_value=None, new_format: str = TimeConst.Format.FORMAT_DD_MM_YY):
        return datetime.strptime(time_value, new_format)

    @staticmethod
    def convert_old_date_to_new_date_by_format(time_value=None, new_format: str = TimeConst.Format.FORMAT_DD_MM_YY_DD_Z, dt_format: str = TimeConst.Format.FORMAT_DD_MM_YYYY):
        return datetime.strptime(time_value, new_format).strftime(dt_format)

    @staticmethod
    def get_future_date_time_by_new_format(number_of_days: int = 1):
        current_day = datetime.today()
        feature_datetime = current_day + timedelta(days=number_of_days)
        return feature_datetime

    @staticmethod
    def get_current_unix_timestamp() -> str:
        """
        :return: string of datetime in unix format
        :rtype:
        """
        time.sleep(1)
        return str(int(time.time()))
    
    @staticmethod
    def get_begin_and_last_date_of_month(month: int, year: int = datetime.now().year):
        """_summary_
        this method will return list of 2 string: begining of the month and last day of the month
        each string will be formatted as dd/mm/yyy e.g:01/04/2024 
        output: [01/04/2024, 30/04/2024]
        Args:
            month (str): _description_
            year (str, optional): _description_. Defaults to datetime.now().year.
        """
        import datetime
        eom = calendar.monthrange(year, month)[1]
        return [datetime.date(year, month, 1).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY), 
                datetime.date(year, month, eom).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY)]
    
   
