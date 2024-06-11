"""IQD Diagnostics exceptions."""


class InvalidDiagnosticsDataError(ValueError):
    """Invalid diagnostics data error.

    Raised if processed data is not valid diagnostics data.
    """


class UnsupportedDiagnosticsVersionError(ValueError):
    """Unsupported diagnostics version error.

    Raised if diagnostics version value is unknown.
    """


class InvalidDiagnosticsDataLengthError(ValueError):
    """Invalid diagnostics data length error.

    Raised if diagnostics data version is supported, but the data length does not match expected data length.
    """
