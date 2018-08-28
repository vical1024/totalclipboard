import ctypes
from ctypes import wintypes
import pythoncom
import win32clipboard


class DROPFILES(ctypes.Structure):
    _fields_ = (('pFiles', wintypes.DWORD),
                ('pt', wintypes.POINT),
                ('fNC', wintypes.BOOL),
                ('fWide', wintypes.BOOL))


def clip_files(file_list):
    offset = ctypes.sizeof(DROPFILES)
    length = sum(len(p) + 1 for p in file_list) + 1
    size = offset + length * ctypes.sizeof(ctypes.c_wchar)
    buf = (ctypes.c_char * size)()
    df = DROPFILES.from_buffer(buf)
    df.pFiles, df.fWide = offset, True
    for path in file_list:
        print("copying to clipboard, filename = " + path)
        array_t = ctypes.c_wchar * (len(path) + 1)
        path_buf = array_t.from_buffer(buf, offset)
        path_buf.value = path
        offset += ctypes.sizeof(path_buf)
    stg = pythoncom.STGMEDIUM()
    stg.set(pythoncom.TYMED_HGLOBAL, buf)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    try:
        print(stg)
        print(stg.data)
        win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, stg.data)
        print("clip_files() succeed")
    finally:
        win32clipboard.CloseClipboard()
