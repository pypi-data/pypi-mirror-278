# This file is part of mesibo Python SDK for various platforms.
#         
# By accessing and utilizing this work, you hereby acknowledge that you have thoroughly 
# reviewed, comprehended, and commit to adhering to the terms and conditions stipulated 
# on the mesibo website, thereby entering into a legally binding agreement.
# 
# https://mesibo.com
#
# Copyright (c) 2019-Present Mesibo Inc, Palo Alto, United States
# All rights reserved.
#  



__mesibo_version__ = '2.5.2'


import ctypes
import platform
import multiprocessing
import sys
import os
import warnings
import inspect
import filecmp

def system_exit_error(err):
    info = "\nSystem: " + platform.system().lower() +  "\nPlatform: " + platform.machine() + "\nVersion: " + get_version_folder() + "\n" + "mesibo: " + __mesibo_version__;
    raise SystemExit(info + "\n\n==> Error: " + err + "\n")

def get_version_folder():
    return platform.python_version_tuple()[0] + "." + platform.python_version_tuple()[1]

def get_system():
    system = platform.system().lower()
    if("" == system):
        system = "unknown"

    if("cygwin" in system):
        system = "windows"

    if("darwin" in system):
        system = "macos"

    return system

def get_platform_folder():
    system = get_system()

    machine = platform.machine()
    if("" == machine):
        machine = "unknown"

    if(machine.lower() == "amd64"):
        machine = "x86_64"

    return os.path.join(system.lower(), machine.lower())

def get_mesibo_lib():
    system = get_system()
    lib = "libmesibo.so"
    if(system == "windows"):
        lib = "mesibo.dll"
    return lib

def get_pymesibo_lib():
    system = get_system()
    lib = "_mesibo.so"
    if(system == "windows"):
        lib = "_mesibo.pyd"
    system = platform.system().lower()
    if("cygwin" in system):
        lib = "_mesibo.dll"
    return lib

def get_pymesibo_checksum():
    return "_mesibo.sum"

CLIB_DIR = "clib"
def get_full_path_to_lib():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    clib_dir = os.path.join(package_dir, CLIB_DIR)
    platform_lib = get_platform_folder()
    lib_path = os.path.join(clib_dir, platform_lib)
    return lib_path

def get_pymesibo_path():
    path = get_full_path_to_lib()
    path = os.path.join(path, get_version_folder())
    return path

def set_path_to_lib():
    sys.path.append(get_pymesibo_path());

def get_mesibo_lib_path():
    path = get_full_path_to_lib()
    return os.path.join(path, get_mesibo_lib())

def get_pymesibo_lib_path():
    path = get_pymesibo_path()
    return os.path.join(path, get_pymesibo_lib())

def get_python_lib_path():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(package_dir, get_pymesibo_lib())

def get_pymesibo_checksum_path():
    path = get_pymesibo_path()
    return os.path.join(path, get_pymesibo_checksum())

def get_python_checksum_path():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(package_dir, get_pymesibo_checksum())

def excepthook(type, value, traceback):
    print(value)

def is_installed():
    if not os.path.exists(get_pymesibo_checksum_path()):
        return False
    if not os.path.exists(get_pymesibo_lib_path()):
        return False
    return True

def is_copied():
    if not os.path.exists(get_python_lib_path()):
        return False

    pypath = get_python_checksum_path()
    mesibopath = get_pymesibo_checksum_path()
    if not os.path.exists(pypath):
        return False

    try:
        filecmp.clear_cache()
        return filecmp.cmp(pypath, mesibopath, False)
    except Exception:
        return False

def copy_files():
    if(is_copied()):
        return

    pypath = get_python_checksum_path()
    mesibopath = get_pymesibo_checksum_path()

    import shutil
    try:
        shutil.copy2(mesibopath, pypath)
        pypath = get_python_lib_path()
        mesibopath = get_pymesibo_lib_path()
        shutil.copy2(mesibopath, pypath)
    except Exception:
        pass

    if(is_copied()):
        return

    sys.excepthook = excepthook
    mesibopath = get_pymesibo_path()
    package_dir = os.path.dirname(os.path.realpath(__file__))
    error = "mesibo requires following file to be copied. Execute the following command to copy and try again:\n\n $ sudo /bin/cp -f " + mesibopath + "/* " + package_dir + "/\n";
    system_exit_error(error)


if not is_installed():
    error = "missing files. Please uninstall and install mesibo again\n";
    system_exit_error(error)

set_path_to_lib();
copy_files();


if __package__ or "." in __name__:
    from ._mesibo import *
else:
    from _mesibo import *

def _get_raw_string(s):
    if(not s):
        s = ""
    return s.encode('raw_unicode_escape')

_mesibo_lib = get_mesibo_lib_path()

python_version = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)

system = platform.system().lower()
if("cygwin" in system):
    if 'CYGWINPATH' in os.environ:
        cygpath = os.environ['CYGWINPATH']
        _mesibo_lib = cygpath + _mesibo_lib
    else:
        _mesibo_lib = os.path.relpath(_mesibo_lib)

if(0 != mesibo_init(_mesibo_lib, __mesibo_version__, python_version)):
    system_exit_error('Unable to load: '+ _mesibo_lib + ' Platform not supported. Contact us at https://mesibo.com/support')

def getMesiboInstance():
    return createMesiboInstance();



