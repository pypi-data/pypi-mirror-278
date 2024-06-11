"""
maix.time module
"""
from __future__ import annotations
__all__ = ['DateTime', 'gmtime', 'localtime', 'now', 'sleep', 'sleep_ms', 'sleep_us', 'strptime', 'time', 'time_diff', 'time_ms', 'time_s', 'time_us']
class DateTime:
    day: int
    hour: int
    microsecond: int
    minute: int
    month: int
    second: int
    weekday: int
    year: int
    yearday: int
    zone: float
    zone_name: str
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0, yearday: int = 0, weekday: int = 0, zone: int = 0) -> None:
        ...
    def strftime(self, format: str) -> str:
        """
        Convert to string
        
        Returns: date time string
        """
    def timestamp(self) -> float:
        """
        Convert to float timestamp
        
        Returns: float timestamp
        """
def gmtime(timestamp: float) -> DateTime:
    """
    timestamp to DateTime(time zone is UTC (value 0))
    
    Args:
      - timestamp: double timestamp
    
    
    Returns: DateTime
    """
def localtime() -> DateTime:
    """
    Get local time
    
    Returns: local time, DateTime type
    """
def now() -> DateTime:
    """
    Get current UTC date and time
    
    Returns: current date and time, DateTime type
    """
def sleep(s: float) -> None:
    """
    Sleep seconds
    
    Args:
      - s: seconds, double type
    """
def sleep_ms(ms: int) -> None:
    """
    Sleep milliseconds
    
    Args:
      - ms: milliseconds, uint64_t type
    """
def sleep_us(us: int) -> None:
    """
    Sleep microseconds
    
    Args:
      - us: microseconds, uint64_t type
    """
def strptime(str: str, format: str) -> DateTime:
    """
    DateTime from string
    
    Args:
      - str: date time string
      - format: date time format
    
    
    Returns: DateTime
    """
def time() -> float:
    """
    Get current time in s
    
    Returns: current time in s, double type
    """
def time_diff(last: float, now: float = -1) -> float:
    """
    Calculate time difference
    
    Args:
      - last: last time
      - now: current time
    
    
    Returns: time difference
    """
def time_ms() -> int:
    """
    Get current time in ms
    
    Returns: current time in ms, uint64_t type
    """
def time_s() -> int:
    """
    Get current time in s
    
    Returns: current time in s, uint64_t type
    """
def time_us() -> int:
    """
    Get current time in us
    
    Returns: current time in us, uint64_t type
    """
