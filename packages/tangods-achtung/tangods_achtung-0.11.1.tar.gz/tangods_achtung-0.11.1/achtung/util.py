import logging
import json
from typing import Dict, Union, Optional

"""
Utility functions
"""


class Timer:
    """ A timing statistic collector """

    def __init__(self):
        self.maximum = None
        self.minimum = None
        self.total_time = 0
        self.count = 0

    @property
    def average(self) -> Optional[float]:
        if self.count:
            return self.total_time / self.count
        else:
            return None

    def add(self, t: Union[int, float]) -> None:
        self.total_time += t
        self.count += 1
        if self.maximum is None:
            self.maximum = t
        else:
            self.maximum = max(self.maximum, t)
        if self.minimum is None:
            self.minimum = t
        else:
            self.minimum = min(self.minimum, t)

    def as_dict(self) -> Dict[str, Optional[Union[int, float]]]:
        return {
            "average": self.average,
            "maximum": self.maximum,
            "minimum": self.minimum,
            "total_time": self.total_time,
            "count": self.count
        }


class JsonFormatter(logging.Formatter):
    """
    Formats log records as JSON strings.
    """

    def format(self, record) -> str:
        return json.dumps(record, default=str)
