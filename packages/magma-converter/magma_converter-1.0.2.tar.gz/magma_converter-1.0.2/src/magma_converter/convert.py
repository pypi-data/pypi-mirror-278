import os
import numpy as np
from datetime import timedelta
from obspy import read, Stream, UTCDateTime
from typing import Any, Dict, Self
from .sds import SDS
from .utilities import (
    validate_dates,
    validate_directory_structure,
    trimming_trace
)


class Convert:
    def __init__(self, input_dir: str, directory_structure: str, network: str = 'VG',
                 station: str = '*', channel: str = '*', location: str = '*', output_directory: str = None,):
        """Seismic convert class

        Convert CVGHM various seismic data structure into Seiscomp Data Structure (SDS)

        Args:
            input_dir (str): input directory path
            directory_structure (str): input directory structure
            network (str): input network name
            station (str): input station name
            channel (str): input channel name
            location (str): input location name
        """
        self.new_channel: str | None = None
        self.start_date: np.datetime64 | None = None
        self.end_date: np.datetime64 | None = None
        self.date_str: str | None = None
        self.directory_structure = validate_directory_structure(directory_structure)
        self.input_dir = input_dir
        self.output_dir = output_directory
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.select = {
            'network': network,
            'station': station,
            'location': location,
            'component': channel,
        }
        self.success: list[Dict[str, Any]] = []
        self.failed: list[Dict[str, Any]] = []

    def merged(self, stream: Stream) -> Stream:
        """Merging seismic data into daily seismic data.

        Args:
            stream (Stream): Stream object

        Returns:
            Stream: Stream object
        """
        start_time: UTCDateTime = UTCDateTime(self.date_str)
        end_time: UTCDateTime = UTCDateTime(self.date_str) + timedelta(days=1)
        return trimming_trace(stream, start_time, end_time)

    def seisan(self) -> Stream:
        """Read seisan data structure.

        Returns:
            Stream: Stream object
        """
        import warnings
        warnings.filterwarnings("error")

        wildcard: str = "{}*".format(self.date_str)
        seismic_dir: str = os.path.join(self.input_dir, wildcard)

        try:
            stream: Stream = read(seismic_dir)
            stream = stream.select(**self.select)
            return stream
        except Exception as e:
            print(f'⛔ {self.date_str} - self.seisan():: {e}')
            return Stream()

    def search(self, date_str: str = None) -> Stream:
        """Search seismic data structure.

        Returns:
            Stream: Stream object
        """
        stream: Stream = Stream()

        if date_str is None:
            date_str = self.date_str

        if self.directory_structure in ['ibu', 'seisan']:
            stream = self.seisan()
            print(f"👍 {date_str} :: Total {stream.count()} traces found.")

        return self.merged(stream)

    def from_date(self, start_date: str) -> Self:
        """Set start date.

        Args:
            start_date (str): start date

        Returns:
            Self: Convert class
        """
        self.start_date = np.datetime64(start_date)
        return self

    def to_date(self, end_date: str) -> Self:
        """Set end date.

        Args:
            end_date (str): end date

        Returns:
            Self: Convert class
        """
        self.end_date = np.datetime64(end_date)
        return self

    def fix_channel_to(self, new_channel: str) -> Self:
        """Fix channel name

        Args:
            new_channel (str): new channel name

        Returns:
            Self: Convert class
        """
        self.new_channel = new_channel
        return self

    def run(self, min_completeness: float = 70.0, **kwargs) -> Self:
        """Run seismic converter.

        Args:
            min_completeness (float): minimum completeness value. Default is 70.0%

        Returns:
            Self: Convert class
        """
        print('Converting...')
        validate_dates(self.start_date, self.end_date)
        dates = np.arange(self.start_date, self.end_date,
                          np.timedelta64(1, 'D'))

        for date_str in dates:
            self.date_str = str(date_str)
            for trace in self.search():
                sds: SDS = SDS(
                    output_dir=self.output_dir,
                    trace=trace,
                    channel=self.channel,
                    station=self.station,
                    location=self.location,
                    network=self.network,
                )

                if sds.save(min_completeness=min_completeness, **kwargs):
                    self.success.append(sds.results)
                else:
                    self.failed.append(sds.results)

        return self
