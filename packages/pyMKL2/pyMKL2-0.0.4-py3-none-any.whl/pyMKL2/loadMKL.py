import ctypes
from ctypes import CDLL, RTLD_GLOBAL
from ctypes.util import find_library
import sys, os
import glob

platform = sys.platform

libname = {'linux': 'libmkl_rt.so',  # works for python3 on linux
           'linux2': 'libmkl_rt.so',  # works for python2 on linux
           'darwin': 'libmkl_rt.dylib',
           'win32': 'mkl_rt.dll'}


def _loadMKL():
    libmkl = None
    mkl_rt = find_library('mkl_rt')
    if mkl_rt is None:
        mkl_rt = find_library('mkl_rt.1')

    if mkl_rt is None:
        mkl_rt_path = sorted(
            glob.glob(f'{sys.prefix}/[Ll]ib*/**/*mkl_rt*', recursive=True),
            key=len
        )
        for path in mkl_rt_path:
            try:
                libmkl = ctypes.CDLL(path)
                break
            except (OSError, ImportError):
                pass

        if libmkl is None:
            raise ImportError('mkl_rt not found')
    else:
        libmkl = ctypes.CDLL(mkl_rt)

    return libmkl