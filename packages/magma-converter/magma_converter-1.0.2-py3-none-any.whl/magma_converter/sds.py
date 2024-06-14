import os
from obspy import Trace
from datetime import datetime
from typing import Any, Dict, Tuple, Self
from .new_trace import NewTrace


class SDS(NewTrace):
    """The basic directory and file layout is defined as:
    <SDS dir>/Year/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY

    Structure:

        SDS dir 	:  arbitrary base directory
        YEAR 	:  4 digit year
        NET 	:  Network code/identifier, up to 8 characters, no spaces
        STA 	:  Station code/identifier, up to 8 characters, no spaces
        CHAN 	:  Channel code/identifier, up to 8 characters, no spaces
        TYPE 	:  1 characters indicating the data type, recommended types are:
                    'D' - Waveform data
                    'E' - Detection data
                    'L' - Log data
                    'T' - Timing data
                    'C' - Calibration data
                    'R' - Response data
                    'O' - Opaque data
        LOC 	:  Location identifier, up to 8 characters, no spaces
        DAY 	:  3 digit day of year, padded with zeros

    The dots, '.', in the file names must always be present regardless if
    neighboring fields are empty.

    Additional data type flags may be used for extended structure definition
    """

    def __init__(self, trace: Trace, output_dir: str = None, date_str: str = None,
                 station: str = None, channel: str = None, network: str = 'VG', location: str = '00'):

        channel = None if channel == '*' else channel
        station = None if station == '*' else station
        location = '00' if location == '*' else location
        network = 'VG' if network == '*' else network

        super().__init__(trace, station=station, channel=channel,
                         network=network, location=location)

        self._results = None

        if output_dir is None:
            output_dir = os.path.join(os.getcwd())
        output_dir = os.path.join(output_dir, 'SDS')
        os.makedirs(output_dir, exist_ok=True)

        self.output_dir: str = output_dir

        if date_str is None:
            date_str = trace.stats.starttime.strftime('%Y-%m-%d')
        self.date_str: str = date_str

        self.date_obj: datetime = datetime.strptime(self.date_str, '%Y-%m-%d')
        self.julian_date: str = self.date_obj.strftime('%j')

    @property
    def structure(self) -> Dict[str, str]:
        """The basic structure directory and file layout is defined as:
        <SDS dir>/Year/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY

        :return: :class:`Dict[str, str]`
        """
        return dict(year=self.trace.stats.starttime.strftime('%Y'),
                    network=self.trace.stats.network,
                    station=self.trace.stats.station,
                    channel=self.trace.stats.channel,
                    type='D',
                    location=self.trace.stats.location,
                    julian_date=self.julian_date)

    @property
    def filename(self) -> str:
        """Returns the trace filename

        :return: :class:`str`
        """
        return '.'.join([
            self.structure['network'],
            self.structure['station'],
            self.structure['location'],
            self.structure['channel'],
            self.structure['type'],
            self.structure['year'],
            self.structure['julian_date']
        ])

    @property
    def path(self) -> str:
        """Returns the relative SDS path

        :return: :class:`str`
        """
        return os.path.join(
            self.output_dir,
            self.structure['year'],
            self.structure['network'],
            self.structure['station'],
            self.structure['channel'] + '.' + self.structure['type']
        )

    @property
    def relative_path(self) -> str:
        """Returns the relative SDS path

        :return: :class:`str`
        """
        return os.path.join(
            self.structure['year'],
            self.structure['network'],
            self.structure['station'],
            self.structure['channel'] + '.' + self.structure['type']
        )

    @property
    def full_path(self) -> str:
        """Returns full path of the trace file

        :return: :class:`str`
        """
        return os.path.join(
            self.output_dir,
            self.path,
            self.filename
        )

    @property
    def directories(self) -> Tuple[str, str, str, str]:
        """Returns the full path of the SDS directory

        :return: a tuple of string of filename, path, and full_path
        :rtype: (string, string, string)
        """
        return self.filename, self.path, self.full_path, self.relative_path

    @property
    def results(self) -> dict[str, Any]:
        """Get the metadata of the trace.

        Returns:
            dict[str, Any]: Metadata.
        """
        return self._results

    @results.setter
    def results(self, file_location: str = None) -> None:
        """Set the metadata of the new trace.

        Args:
            file_location (str): The location of the trace file
        """
        self._results: dict[str, Any] = dict(
            trace_id=self.trace.id,
            start_date=self.trace.stats.starttime.strftime('%Y-%m-%d'),
            end_date=self.trace.stats.endtime.strftime('%Y-%m-%d'),
            start_time=self.trace.stats.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            end_time=self.trace.stats.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            sampling_rate=self.trace.stats.sampling_rate,
            completeness=self.completeness,
            file_location=file_location
        )

    def save(self, min_completeness: float = 70.0, encoding: str = 'STEIM2', **kwargs) -> bool:
        """Save into SDS

        Args:
            encoding (str): encoding type. Default STEIM2
            min_completeness (float): minimum completeness value to be saved

        Returns:
            Self: Convert class
        """
        self.results = None

        if os.path.isfile(self.full_path):
            print(f"✅ {self.date_str} :: {self.trace.id} already exists: {self.full_path}")
            self.results = self.full_path
            return True

        if self.completeness > min_completeness:
            os.makedirs(
                os.path.join(self.output_dir, self.path),
                exist_ok=True
            )

            self.trace.write(self.full_path, format='MSEED', encoding=encoding, **kwargs)
            self.results = self.full_path
            print(f'✅ {self.date_str} :: {self.trace.id} completeness: {self.completeness:.2f}% ➡️ {self.full_path}')
            return True

        print(f'⛔ {self.date_str} :: {self.trace.id} Not saved. Trace completeness '
              f'{self.completeness:.2f}%! Below {min_completeness}%')
        return False
