import enum
import os
import platform


@enum.unique
class DisplayServer(enum.Enum):
    wayland = "wayland"
    x11 = "x11"


class Config:
    ARCH = platform.machine()

    PASSWORD = "1"

    DISPLAY_SERVER = (
                         os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
                         .read()
                         .split("=")[-1]
                         .strip("\n")
                     ) or ("x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland")

    IS_X11 = DISPLAY_SERVER == DisplayServer.x11.value
    IS_WAYLAND = DISPLAY_SERVER == DisplayServer.wayland.value


conf = Config()
