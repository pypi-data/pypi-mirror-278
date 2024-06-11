"""
Constants for the CLI.
"""

from enum import Enum
import platform

__VERSION__ = "0.0.1"


class ProjectType(str, Enum):
    if platform.system() == "Windows":
        make = "make"
        ninja = "ninja"
        vs = "vs"
    else:
        make = "make"
        ninja = "ninja"


class CompilerVersion(str, Enum):
    if platform.system() == "Windows":
        vs_16 = 16
        vs_17 = 17
    else:
        gcc_11 = 11
        gcc_10 = 10
        gcc_9 = 9


class Arch(str, Enum):
    x86_64 = "x86_64"
    x86 = "x86"


class BuildType(str, Enum):
    releasewithdebinfo = "RelWithDebInfo"
    release = "Release"
    debug = "Debug"
    rd = "rd"
    r = "r"
    d = "d"
