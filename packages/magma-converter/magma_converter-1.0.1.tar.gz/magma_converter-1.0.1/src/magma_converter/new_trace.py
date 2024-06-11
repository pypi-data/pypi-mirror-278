import numpy as np
from obspy import Trace


def fix_station(trace: Trace, station: str = None) -> str:
    """Fix station name.

    Args:
        trace (Trace): Trace to fix.
        station (str): Station name.

    Returns:
        str: Station name.
    """
    if station is not None:
        return station

    if trace.stats.station:
        return trace.stats.station


def fix_channel(trace: Trace, channel: str = None) -> str:
    """Get name and fix channel name.

    Args:
        trace (Trace): Trace to fix.
        channel (str): Channel name.

    Returns:
        str: Fixed channel name.
    """
    if channel is not None:
        return channel

    if 'EHZ' == trace.stats.channel:
        return 'EHZ'

    # For Ijen
    if 'BH' in trace.stats.channel:
        return 'BH{}'.format(trace.stats.location)

    if 'Z' in trace.stats.location:
        return 'EHZ'
    if 'Z' in trace.stats.channel:
        return 'EHZ'
    if 'N' in trace.stats.channel:
        return 'EHN'
    if 'E' in trace.stats.channel:
        return 'EHE'
    # if self.structure_type == 'win_sinabung':
    #     stations = config['type']['win_sinabung']['stations']
    #     return stations[self.trace.stats.channel]['channel']
    return 'EHZ'


class NewTrace:
    def __init__(self, trace: Trace, station: str = None,
                 channel: str = None, network: str = 'VG', location: str = '00'):
        self.station = fix_station(trace, station).upper()
        self.channel = fix_channel(trace, channel).upper()
        self.network = network.upper()
        self.location = location.upper()
        self.trace = self.new_trace(trace)

    def new_trace(self, trace: Trace) -> Trace:
        trace.data = np.where(trace.data == -2 ** 31, 0, trace.data)
        trace.data = trace.data.astype(np.int32)
        trace.stats['station'] = self.station
        trace.stats['network'] = self.network
        trace.stats['channel'] = self.channel
        trace.stats['location'] = self.location

        return trace

    @property
    def completeness(self) -> float:
        """Get the non-zero values of completeness of the new trace.

        Returns:
            float: Completeness of the trace.
        """
        return (np.count_nonzero(self.trace.data) / 8640000) * 100
