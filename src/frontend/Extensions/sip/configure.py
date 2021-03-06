#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import os
import sipconfig
import subprocess
from PyQt5.Qt import PYQT_CONFIGURATION


def getQtPath(name):
    result = subprocess.check_output(["qmake-qt5", "-query", name], universal_newlines = True)
    result = result.replace("\n", "")
    return result

# The name of the SIP build file generated by SIP and used by the build
# system.
build_file = "DBusTypes.sbf"

# Get the SIP configuration information.
config = sipconfig.Configuration()

# Run SIP to generate the code.
os.system(" ".join([
    config.sip_bin, "-c", ".", "-b", build_file,
    "-I", "/usr/share/sip/PyQt5",
    "-I", "/usr/share/python3-sip/PyQt5",
    PYQT_CONFIGURATION["sip_flags"],
    "DBusTypes.sip",
]))

# Create the Makefile.
makefile = sipconfig.SIPModuleMakefile(config, build_file)

# Add the library we are wrapping.  The name doesn't include any platform
# specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
# ".dll" extension on Windows).
makefile.extra_libs = ["Qt5DBus", "Qt5Core", "DBusTypes", ]
makefile.extra_include_dirs = [
    getQtPath("QT_INSTALL_HEADERS"),
    getQtPath("QT_INSTALL_HEADERS") + "/QtCore",
]

# extra_lib_dirs enables sip to find the C++ shared library
# we also want current dir to be the rpath
rpath = os.path.dirname(os.getcwd())
makefile.extra_lflags = ["-Wl,-rpath {}".format(rpath)]
makefile.extra_lib_dirs = ["../"]

# Generate the Makefile itself.
makefile.generate()
