from __future__ import annotations

import ctypes
import hashlib
import msvcrt
import os
import sys
from ctypes import wintypes
from typing import Union

from ok.util.path import get_path_relative_to_exe

# Define necessary constants and functions
ERROR_ALREADY_EXISTS = 183
NULL = 0
LPSECURITY_ATTRIBUTES = wintypes.LPVOID
BOOL = ctypes.c_int
DWORD = ctypes.c_ulong
HANDLE = ctypes.c_void_p
CreateMutex = ctypes.windll.kernel32.CreateMutexW
CreateMutex.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, wintypes.LPCWSTR]
CreateMutex.restype = HANDLE
GetLastError = ctypes.windll.kernel32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = DWORD


def check_mutex():
    path = get_path_relative_to_exe()
    # Try to create a named mutex
    path = hashlib.md5(path.encode()).hexdigest()
    mutex = CreateMutex(NULL, False, f"{path}")

    # Check if the mutex already exists
    if GetLastError() == ERROR_ALREADY_EXISTS:
        print(f"Another instance of this application is already running. {path}")
        sys.exit(0)


def all_pids() -> list[int]:
    pidbuffer = 512
    bytes_written = ctypes.c_uint32()
    while True:
        pids = (ctypes.c_uint32 * pidbuffer)()
        bufsize = ctypes.sizeof(pids)
        if ctypes.windll.kernel32.K32EnumProcesses(pids, bufsize, ctypes.byref(bytes_written)) == 0:
            return []
        if bytes_written.value < bufsize:
            break
        pidbuffer *= 2
    pidcount = bytes_written.value // 4
    return list(pids[:pidcount])


NtQuerySystemInformation = ctypes.windll.ntdll.NtQuerySystemInformation
NtQuerySystemInformation.argtypes = (ctypes.c_int32, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))
SystemProcessIdInformation = 0x58


class UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ('Length', ctypes.c_ushort),
        ('MaximumLength', ctypes.c_ushort),
        ('Buffer', ctypes.c_wchar_p),
    ]

    @classmethod
    def create(cls, init_with: Union[str, int]):
        buffer = ctypes.create_unicode_buffer(init_with)
        bufsize = len(buffer)
        if isinstance(init_with, str):
            wchlen = bufsize - 1  # exclude null
        else:
            wchlen = 0
        return cls(wchlen * 2, bufsize * 2, ctypes.cast(buffer, ctypes.c_wchar_p))

    def __str__(self):
        return ctypes.wstring_at(self.Buffer, self.Length // 2)


class SYSTEM_PROCESS_ID_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('ProcessId', ctypes.c_size_t),
        ('ImageName', UNICODE_STRING),
    ]


def resolve_image_name(pid: int):
    """Resolves the image name of a process, in NT device path (\\Device\\HarddiskVolumeX\\...) format."""
    info = SYSTEM_PROCESS_ID_INFORMATION()
    info.ProcessId = pid
    status = NtQuerySystemInformation(SystemProcessIdInformation, ctypes.byref(info), ctypes.sizeof(info), None)
    if status == -1073741820:
        info.ImageName = UNICODE_STRING.create(info.ImageName.MaximumLength // 2)
        status = NtQuerySystemInformation(SystemProcessIdInformation, ctypes.byref(info), ctypes.sizeof(info), None)
        return str(info.ImageName)
    else:
        return ''


GetFinalPathNameByHandleW = ctypes.windll.kernel32.GetFinalPathNameByHandleW
GetFinalPathNameByHandleW.argtypes = (ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32)


def get_final_path(path: os.PathLike) -> str:
    with open(path, 'rb', buffering=0) as f:
        handle = msvcrt.get_osfhandle(f.fileno())
        buf = ctypes.create_unicode_buffer(32768)
        pathlen = GetFinalPathNameByHandleW(handle, buf, 32768, 2)
        if pathlen == 0:
            raise ctypes.WinError()
        return buf[:pathlen]


def _test():
    for pid in all_pids():
        print(pid, resolve_image_name(pid), sep='\t')
