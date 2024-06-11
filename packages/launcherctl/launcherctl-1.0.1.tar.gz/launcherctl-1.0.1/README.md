[![launcherctl on PyPI](https://img.shields.io/pypi/v/launcherctl)](https://pypi.org/project/launcherctl)

Python wrapper around launcherctl
=================================

Installation
============

```bash
pip install launcherctl
```

Usage
=====

```python
import launcherctl

if (
    launcherctl.launchers.current.name != "oxide"
    and "oxide" in launcherctl.launchers
):
    launcherctl.launchers.switch("oxide", start=True)
    # or
    launcherctl.launchers["oxide"].enable(start=True)

if (
    "calculator" in launcherctl.apps
    and "calculator" not in launcherctl.apps.running.keys()
):
    launcherctl.apps["calculator"].start()
```
