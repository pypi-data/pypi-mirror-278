import subprocess


def LauncherCtlException(Exception):
    pass


def launcherctl(*args) -> str | None:
    try:
        return subprocess.check_output(["/opt/bin/launcherctl"] + list(args))
    except subprocess.CalledProcessError as e:
        stdout = e.output.decode("utf-8")
        raise LauncherCtlException(stdout) from e
