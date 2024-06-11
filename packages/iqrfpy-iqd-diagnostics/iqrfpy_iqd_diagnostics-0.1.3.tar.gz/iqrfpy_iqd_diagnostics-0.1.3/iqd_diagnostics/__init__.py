"""IQD Diagnostics.

.. include:: ../README.md

.. include:: ../changelog.md
"""

from __future__ import annotations

from .constants import (
    DIAGNOSTICS_HEADER_VALUE,
)

from .exceptions import (
    InvalidDiagnosticsDataError,
    InvalidDiagnosticsDataLengthError,
    UnsupportedDiagnosticsVersionError,
)

from .iqd_diagnostics import (
    IqdDiagnostics,
)

from .objects import (
    DiagnosticsVersion,
    DiagnosticsResolver,
)

__all__ = (
    # .constants
    'DIAGNOSTICS_HEADER_VALUE',
    # .exceptions
    'InvalidDiagnosticsDataError',
    'InvalidDiagnosticsDataLengthError',
    'UnsupportedDiagnosticsVersionError',
    # .diagnostics
    'IqdDiagnostics',
    # .objects
    'DiagnosticsVersion',
    'DiagnosticsResolver',
)
