"""This is the tool used to parse common-used command line arguments for Kasheesh ETLs.
"""


import argparse
from pandas import to_datetime, Timedelta, Timestamp
from kasheesh_tools.tool_logger import get_my_logger

class ToolCmdParser:
    def __init__(self, name='ToolCmdParser'):
        """* no arguments given: full history
           * only given start_date: data on and after start_date
           * only given end_date: data on and before end_date
           * only given --scheduled_job: data on current date
           * given mixed start_date/end_date & scheduled_job: start_date/end_date will be ignored and only run data on current date

        Args:
            name (str, optional): _description_. Defaults to 'ToolCmdParser'.
        """
        self.logger = get_my_logger(name=name)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--start_date', type=str, help='starting created date of the transactions')
        self.parser.add_argument('--end_date', type=str, help='ending created date of the transactions')
        self.parser.add_argument('--scheduled_job', type=bool, help='whether this is a scheduled job', action=argparse.BooleanOptionalAction)
        self.args = self.parser.parse_args()

    def _get_start_date(self):
        if self.args.start_date:
            if self.args.scheduled_job:
                self.logger.warning('start_date will be ignored for scheduled job.')
            self.start_date = to_datetime(self.args.start_date).date()
        else:
            self.start_date = None
        self.logger.info(f'start_date: {self.start_date}')

    def _get_end_date(self):    
        if self.args.end_date:
            if self.args.scheduled_job:
                self.logger.warning('end_date will be ignored for scheduled job.')
            self.end_date = to_datetime(self.args.end_date).date()
        else:
            self.end_date = None
        self.logger.info(f'end_date: {self.end_date}')

    def _get_scheduled_job(self):
        if self.args.scheduled_job:
            self.scheduled_job = True
            standard_date = Timestamp.utcnow().date()
            self.start_date = standard_date - Timedelta(days=1)
            self.end_date = standard_date - Timedelta(days=1)
        else:
            self.scheduled_job = False
        self.logger.info(f'scheduled_job: {self.scheduled_job}')

    def get_args(self):
        self._get_start_date()
        self._get_end_date()
        self._get_scheduled_job() # this will override the start_date and end_date if it's a scheduled job
        return