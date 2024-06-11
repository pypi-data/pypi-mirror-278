# np-aind-metadata



[![PyPI](https://img.shields.io/pypi/v/np-aind-metadata.svg?label=PyPI&color=blue)](https://pypi.org/project/np-aind-metadata/)
[![Python version](https://img.shields.io/pypi/pyversions/np-aind-metadata)](https://pypi.org/project/np-aind-metadata/)

[![Coverage](https://img.shields.io/codecov/c/github/AllenInstitute/np-aind-metadata?logo=codecov)](https://app.codecov.io/github/AllenInstitute/np-aind-metadata)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/AllenInstitute/np-aind-metadata/publish.yml?label=CI/CD&logo=github)](https://github.com/AllenInstitute/np-aind-metadata/actions/workflows/publish.yml)
[![GitHub issues](https://img.shields.io/github/issues/AllenInstitute/np-aind-metadata?logo=github)](https://github.com/AllenInstitute/np-aind-metadata/issues)

# Usage
```bash
conda create -n np_aind_metadata python>=3.10
conda activate np_aind_metadata
pip install np_aind_metadata
```

## On-prem usage
If on Allen Institute premises, additional features are available via `np-config`. To use on-prem features install `np-config`.

```bash
pip install np-config
```

## Python

### On-prem

Copies the latest `rig.json` from storage to a local path. 


```python
>>> from datetime import datetime
>>> from pathlib import Path
>>> import datetime
>>> from np_aind_metadata import rigs

>>> rigs.copy_rig("NP3", datetime(2024, 4, 1), output_path=Path("rig.json"))
PosixPath('rig.json')

```

### Off-prem

Updates a rig json and store it at output path.

```python
>>> from pathlib import Path
>>> from np_aind_metadata.update import update_rig
>>> update_rig(
...     Path(".", "examples", "rig.json"),
...     open_ephys_settings_sources=[
...         Path(
...             ".",
...             "examples",
...             "example-session-directory",
...             "settings.xml"
...         ),
...     ],
...     output_path=Path("rig.json"),
... )
PosixPath('rig.json')

```

### Convenience functions

Direct support for common use cases.

#### np-codeocean

Parses a dynamic routing session directory for a `session.json`, adds it's corresponding `rig.json`, and updates `session.json` to reflect the `rig.json` it is associated with. If not onprem, `rig_storage_dir` will need to be supplied.

```python
>>> from pathlib import Path
>>> from np_aind_metadata.integrations import dynamic_routing_task
>>> session_dir = Path("examples") / "example-session-directory"
>>> dynamic_routing_task.add_rig_to_session_dir(session_dir, datetime.datetime(2024, 4, 1))

```

# Model storage

Models are stored locally on disk. To initialize model storage.

Initialize storage for all supported rigs.

```bash
np-aind-metadata init-rig-storage "/directory/to/store/rigs"
```

Initialize storage for a specific rig.

```bash
np-aind-metadata init-rig-storage "/directory/to/store/rigs" "NP3" --date 2022/02/07
```

Update a stored rig.

```bash
np-aind-metadata update-rig "/directory/to/store/rigs" "NP3" --date 2022/02/07
```

# Local development

## Testing
Testing intended for cloned project from source control.

### Unit tests
```bash
pdm run pytest
```

### Storage tests
```bash
pdm run pytest-storage
```

### On-prem tests
Requires user to likely be on prem with np group dependencies installed.

Install np group dependencies 
```bash
pdm install -G np
```

Run tests
```bash
pdm run pytest-onprem
```

### All tests
Requires dependencies from onprem.
```bash
pdm run pytest-full
```

# Development
See instructions in https://github.com/AllenInstitute/np-aind-metadata/CONTRIBUTING.md and the original template: https://github.com/AllenInstitute/copier-pdm-npc/blob/main/README.md