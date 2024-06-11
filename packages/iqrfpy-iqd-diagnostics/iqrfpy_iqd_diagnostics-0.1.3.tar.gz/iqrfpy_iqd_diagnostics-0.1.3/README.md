## iqrfpy-iqd-diagnostics

An extension for [iqrfpy](https://pypi.org/project/iqrfpy/) for processing and interpreting IQD diagnostics data.

Diagnostics is a common data structure located in the permanent memory of all IQD devices,
which contains the result of the HW test of the device and other operational data that affect its correct operation.

## Quick start

Before installing the library, it is recommended to first create a virtual environment.
Virtual environments help isolate python installations as well as pip packages independent of the operating system.

A virtual environment can be created and launched using the following commands:

```bash
python3 -m venv <dir>
source <dir>/bin/activate
```

iqrfpy-iqd-diagnostics can be installed using the pip utility:

```bash
python3 -m pip install -U iqrfpy-iqd-diagnostics
```

Example use:
```python
from iqrfpy.ext.iqd_diagnostics import IqdDiagnostics

# get iqd_diagnostics data
data = ...

# parse into class
diagnostics = IqdDiagnostics(data=data)

# access values
diagnostics.beaming_cnt

# print formatted data
print(diagnostics.to_string())
```
