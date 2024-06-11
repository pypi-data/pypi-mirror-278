import subprocess

from typing import Callable

from ._app import App
from ._util import launcherctl


class Launcher:
    def __init__(self, name: str):
        self.name = name

    def logs(self, onlogline: Callable[[str], None] = None) -> list[str] | None:
        pass

    def start(self):
        launcherctl("start-launcher", self.name)

    def stop(self):
        launcherctl("stop-launcher", self.name)

    def enable(self, start: bool = False):
        if start:
            launcherctl("switch-launcher", "--start", self.name)

        else:
            launcherctl("switch-launcher", self.name)

    @property
    def is_current(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-current-launcher", self.name])
            == 0
        )

    @property
    def is_enabled(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-enabled-launcher", self.name])
            == 0
        )

    @property
    def is_active(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-active-launcher", self.name])
            == 0
        )


class API:
    def keys(self) -> list[str]:
        return [x.decode("utf-8") for x in launcherctl("list-launchers").splitlines()]

    def __contains__(self, key: str) -> bool:
        return key in self.keys()

    def __getitem__(self, key: str) -> App:
        if key not in self:
            raise KeyError()

        return Launcher(key)

    @property
    def current(self):
        return Launcher(launcherctl("status").splitlines()[0][14:-4].decode("utf-8"))

    def switch(launcher: Launcher | str, start: bool = False):
        if not isinstance(Launcher, launcher):
            launcher = Launcher(launcher)

        launcher.enable(start)


api = API()
