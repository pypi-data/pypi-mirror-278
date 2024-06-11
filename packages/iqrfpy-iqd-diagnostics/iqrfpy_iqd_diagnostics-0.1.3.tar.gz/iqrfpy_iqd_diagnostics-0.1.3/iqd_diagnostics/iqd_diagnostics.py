"""IQD Diagnostics parser (according to the IQD Diagnostics document).

Diagnostics is a common data structure located in the permanent memory of all IQD devices,
which contains the result of the HW test of the device and other operational data that affect its correct operation.
"""
from typing import List

from tabulate import tabulate
from iqrfpy.utils.sensor_constants import SensorTypes
from iqrfpy.utils.sensor_parser import SensorParser, SensorData

from .constants import DIAGNOSTICS_HEADER_VALUE
from .exceptions import InvalidDiagnosticsDataError
from .objects import DiagnosticsResolver, DiagnosticsVersion


class IqdDiagnostics:
    """IQD Diagnostics parser class."""

    __slots__ = ('diagnostics_version', 'errors_archive', 'errors_last', 'beaming_cnt', 'boot_cnt', 'full_lbt_cnt',
                 'local_frc_cnt', 'enter_beaming_cnt', 'online_time', 'min_temperature', 'max_temperature',
                 'min_humidity', 'max_humidity', 'binary_cnt', 'init_voltage', 'min_voltage', 'max_acceleration')

    def __init__(self, data: List[int] = None):
        """IQD Diagnostics parser constructor.

        Args:
            data (List[int]): Diagnostics data byte array.
        """
        if data is None or len(data) < 2:
            raise InvalidDiagnosticsDataError('No diagnostics data to process received.')

        # get diagnostics header
        diagnostics_header = data[0]
        if diagnostics_header != DIAGNOSTICS_HEADER_VALUE:
            raise InvalidDiagnosticsDataError(f'Expected diagnostics header value 0x{DIAGNOSTICS_HEADER_VALUE:02X},'
                                              f' but received 0x{diagnostics_header:02X}')

        # get diagnostics by version
        version = data[1]
        self.diagnostics_version: DiagnosticsVersion = DiagnosticsResolver.get_diagnostics_by_version(version)
        """Diagnostics version."""
        self.diagnostics_version.validate(data)

        self.errors_archive: List[bool] = self.get_flags(data[2:6])
        """Error flags archive."""
        self.errors_last: List[bool] = self.get_flags(data[6:10])
        """Latest error flags."""
        self.beaming_cnt: int = int.from_bytes(data[10:14], byteorder='little')
        """Beaming counter."""
        self.boot_cnt: int = int.from_bytes(data[14:18], byteorder='little')
        """Boot counter."""
        self.full_lbt_cnt: int = int.from_bytes(data[18:22], byteorder='little')
        """Full LBT counter."""
        self.local_frc_cnt: int = int.from_bytes(data[22:26], byteorder='little')
        """Local FRC counter."""
        self.enter_beaming_cnt: int = int.from_bytes(data[26:30], byteorder='little')
        """Enter beaming counter."""
        self.online_time: int = int.from_bytes(data[30:34], byteorder='little')  # [2,56 s]
        """Device uptime."""
        self.min_temperature: SensorData = SensorParser.read_sensors_dpa([SensorTypes.TEMPERATURE], data[34:36])[0]
        """Minimum measurable temperature."""
        self.max_temperature: SensorData = SensorParser.read_sensors_dpa([SensorTypes.TEMPERATURE], data[36:38])[0]
        """Maximum measurable temperature."""
        self.min_humidity: SensorData = SensorParser.read_sensors_dpa([SensorTypes.RELATIVE_HUMIDITY], [data[38]])[0]
        """Minimum measurable humidity."""
        self.max_humidity: SensorData = SensorParser.read_sensors_dpa([SensorTypes.RELATIVE_HUMIDITY], [data[39]])[0]
        """Maximum measurable humidity."""
        self.binary_cnt: int = int.from_bytes(data[40:44], byteorder='little')
        """Binary counter."""
        self.init_voltage: SensorData = SensorParser.read_sensors_dpa([SensorTypes.EXTRA_LOW_VOLTAGE], data[44:46])[0]
        """Initial battery voltage."""
        self.min_voltage: SensorData = SensorParser.read_sensors_dpa([SensorTypes.EXTRA_LOW_VOLTAGE], data[46:48])[0]
        """Minimum battery voltage."""
        self.max_acceleration = SensorParser.read_sensors_dpa([SensorTypes.ACCELERATION], data[48:50])[0]
        """Maximum acceleration."""

    @staticmethod
    def get_flags(data: list[int]) -> list[bool]:
        """Converts bytes into the list of flags True/False.

        Args:
            data (List[int]): Data to convert.

        Returns:
            list[bool]: List of flags.
        """
        flags = []
        bytes_as_int = int.from_bytes(data, byteorder='little')
        for _ in range(len(data) * 8):
            flags.append(bool(bytes_as_int & 0x01))
            bytes_as_int >>= 1
        return flags

    @staticmethod
    def _format_measurement(measurement: SensorData):
        return f'{measurement.value} {measurement.unit}'

    def __str__(self):
        """String representation of diagnostics data.

        Implementation overrides default str() behavior.

        Returns:
            str: Human-readable string representation of diagnostics data.
        """
        version_data = [['Diagnostics Version', self.diagnostics_version.version]]
        errors_headers = ['Errors', 'Archive', 'Last']
        errors_data = [
            ['Low voltage', self.errors_archive[0], self.errors_last[0]],
            ['Accu', self.errors_archive[1], self.errors_last[1]],
            ['Sensor 1', self.errors_archive[2], self.errors_last[2]],
            ['Sensor 2', self.errors_archive[3], self.errors_last[3]],
            ['Sensor 3', self.errors_archive[4], self.errors_last[4]],
            ['Sensor 4', self.errors_archive[5], self.errors_last[5]],
            ['NFC', self.errors_archive[6], self.errors_last[6]],
            ['RAM', self.errors_archive[7], self.errors_last[7]],
            ['Aux MCU', self.errors_archive[8], self.errors_last[8]],
            ['RTC', self.errors_archive[9], self.errors_last[9]],
            ['GPS', self.errors_archive[10], self.errors_last[10]],
        ]
        properties_headers = ['Property', 'Value']
        properties_data = [
            ['Beaming Counter', self.beaming_cnt],
            ['Boot Counter', self.boot_cnt],
            ['Full LBT Counter', self.full_lbt_cnt],
            ['Local FRC Counter', self.local_frc_cnt],
            ['Enter Beaming Counter', self.enter_beaming_cnt],
            ['Online Time', seconds_to_duration(round(self.online_time * 2.56))],
            ['Min. Temperature', self._format_measurement(self.min_temperature)],
            ['Max. Temperature', self._format_measurement(self.max_temperature)],
            ['Min. Humidity', self._format_measurement(self.min_humidity)],
            ['Max. Humidity', self._format_measurement(self.max_humidity)],
            ['Binary Counter', self.binary_cnt],
            ['Init. Voltage', self._format_measurement(self.init_voltage)],
            ['Min. Voltage', self._format_measurement(self.min_voltage)],
            ['Max. Acceleration', self._format_measurement(self.max_acceleration)]
        ]
        version_str = tabulate(headers=[], tabular_data=version_data, tablefmt='double_outline')
        errors_str = tabulate(headers=errors_headers, tabular_data=errors_data, tablefmt='double_outline')
        properties_str = tabulate(headers=properties_headers, tabular_data=properties_data, tablefmt='double_outline')
        return '\n'.join([version_str, errors_str, properties_str])

    def to_string(self):
        """Serializes IQD Diagnostics object to string.

        Formatted as a table of values.

        Returns:
            str: Diagnostics serialized to table format.
        """
        return str(self)


_TIME_DURATION_UNITS = (
    ('year', 60 * 60 * 24 * 365),
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('minute', 60),
    ('second', 1)
)


def seconds_to_duration(seconds: int) -> str:
    """Converts a number of seconds to a formatted string representing the duration.

    Args:
        seconds (int): Number of seconds.

    Returns:
        str: A string containing the time duration.

    Example:
        >>> print(seconds_to_duration(111222333))
        '3 years, 27 weeks, 3 days, 7 hours, 5 mins, 33 secs'
    """
    if seconds == 0:
        return '0 seconds'
    parts = []
    for unit, div in _TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit + "s" if amount > 1 else unit}')
    return ', '.join(parts)
