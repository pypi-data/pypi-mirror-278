"""IQD Diagnostics objects, enums and data classes."""

from dataclasses import dataclass
from typing import List

from .exceptions import InvalidDiagnosticsDataLengthError, UnsupportedDiagnosticsVersionError


@dataclass
class DiagnosticsVersion:
    """Diagnostics version class."""

    __slots__ = 'version', 'data_len'

    def __init__(self, version: int, data_len: int):
        """Diagnostics version constructor.

        Args:
            version (int): Version value.
            data_len (int): Data length.
        """
        self.version = version
        """Diagnostics version."""
        self.data_len = data_len
        """Data length."""

    def validate(self, data: List[int]) -> None:
        """Validate diagnostics data.

        Validates data by length.

        Args:
            data (List[int]): Diagnostics data to validate.

        Raises:
            InvalidDiagnosticsDataLengthError: Raised if diagnostics data length does not match expected data length
                dictated by the version
        """
        tested_data_len = len(data)
        if tested_data_len < self.data_len:
            raise InvalidDiagnosticsDataLengthError(
                f'Length of diagnostics version {self.version} data is at least {self.data_len},'
                f' but the length of received data is {tested_data_len}'
            )


class DiagnosticsResolver:
    """Diagnostics resolver class.

    Diagnostics resolver attempts to find diagnostics version by number.
    """

    _versions = dict(
        [
            (1, DiagnosticsVersion(version=1, data_len=50)),
        ],
    )

    @classmethod
    def get_diagnostics_by_version(cls, version: int) -> DiagnosticsVersion:
        """Get diagnostics version object by version.

        Args:
            version (int): Version value.

        Returns:
            :obj:`DiagnosticsVersion`: Diagnostics version object.

        Raises:
            UnsupportedDiagnosticsVersionError: Raised if version integer value is not supported
        """
        if version in cls._versions:
            return cls._versions[version]
        raise UnsupportedDiagnosticsVersionError(f'Diagnostics version {version} is not supported.')
