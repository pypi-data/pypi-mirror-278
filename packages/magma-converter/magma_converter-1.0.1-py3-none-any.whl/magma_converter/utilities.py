import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
from obspy import Stream, UTCDateTime
from datetime import datetime


directory_structures: Tuple = (
    'seisan',
    'ibu',
    'ruang',
)


def date_to_julian(date_str: str) -> str:
    """Convert date string to Julian date.

    Args:
        date_str (str): date string

    Returns:
        str: Julian date
    """
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%j')


def get_dates(start: str, end: str) -> pd.DatetimeIndex:
    """Get range of dates from start and end dates.

    Args:
        start (str): start date in YYYY-MM-DD format.
        end (str): end date in YYYY-MM-DD format.

    Returns:
        pd.DatetimeIndex: date range.
    """
    return pd.date_range(start, end, freq="D")


def validate_directory_structure(directory_structure: str) -> str | ValueError:
    """Validate that a directory structure.

    Args:
        directory_structure (str):

    Returns:
        str | ValueError
    """
    if directory_structure not in directory_structures:
        raise ValueError(f'{directory_structure} is not a valid archive type. '
                         f'Please chose between {directory_structures}')
    return directory_structure


def validate_dates(start_date: np.datetime64, end_date: np.datetime64) -> bool | ValueError:
    """Validate that the start and end dates.

    Args:
        start_date (np.datetime64): Start date of the date range.
        end_date (np.datetime64): End date of the date range.

    Returns:
        True | ValueError
    """
    if (not isinstance(start_date, np.datetime64)) or (not isinstance(end_date, np.datetime64)):
        raise ValueError(f"start_date or end_date is not set. "
                         f"Please set using from_date() and to_date().")
    return True


def trimming_trace(stream: Stream, start_time: UTCDateTime,
                   end_time: UTCDateTime) -> Stream:
    """Trimm a stream of traces.

    Args:
        stream (Stream): Stream to trim.
        start_time (UTCDateTime): Start time of the date.
        end_time (UTCDateTime): End time of the date.

    Returns:
        Stream: Trimmed stream.
    """
    total_traces = stream.count()
    stream = remove_trace(stream)
    remaining_traces = stream.count()
    removed_traces = total_traces - remaining_traces
    percentage = remaining_traces / total_traces * 100
    print(f"🚮 {start_time.strftime('%Y-%m-%d')} :: {remaining_traces} remaining trace(s) "
          f"({percentage:.2f}%). {removed_traces} BAD trace(s) removed")
    if stream.count() > 0:
        stream.trim(starttime=start_time, endtime=end_time)
        stream.merge(fill_value=0)
    return stream


def remove_trace(stream: Stream) -> Stream:
    """Remove traces from a stream.

    Args:
        stream (Stream): Stream to remove traces from.

    Returns:
        Stream: Stream with traces removed.
    """
    for trace in stream:
        if trace.stats.sampling_rate < 50.0:
            stream.remove(trace)
    return stream


def tree(sds_dir: str = None, prefix: str = ''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters

    Args:
        sds_dir (Path): Directory Path object
        prefix (str, optional): A string to prefix each line with

    Returns:
        None
    """
    sds_dir: Path = Path(sds_dir)
    space: str = '    '
    branch: str = '│   '
    tee: str = '├── '
    last: str = '└── '

    contents: list[Path] = list(sds_dir.iterdir())
    pointers: list[str] = [tee] * (len(contents) - 1) + [last]

    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():
            extension = branch if pointer == tee else space
            yield from tree(path, prefix=prefix + extension)
