# -*- coding: utf-8 -*-
# !python3

import ctypes

text_type = str


def init_windows_clipboard():
    d = ctypes.windll
    CF_UNICODETEXT = 13
    GMEM_DDESHARE = 0x2000

    def copy_windows(text):
        if not isinstance(text, text_type):
            text = text.decode('mbcs')

        d.user32.OpenClipboard(0)
        d.user32.EmptyClipboard()
        hCd = d.kernel32.GlobalAlloc(GMEM_DDESHARE, len(text.encode('utf-16-le')) + 2)
        pchData = d.kernel32.GlobalLock(hCd)

        # Detects this error: "OSError: exception: access violation writing 0x0000000000000000"
        # if pchData == 0:
        #    assert False, 'GlobalLock() returned NULL. GetLastError() returned' + str(ctypes.GetLastError())

        ctypes.cdll.msvcrt.wcscpy(ctypes.c_wchar_p(pchData), text)
        d.kernel32.GlobalUnlock(hCd)
        d.user32.SetClipboardData(CF_UNICODETEXT, hCd)
        d.user32.CloseClipboard()

    def paste_windows():
        d.user32.OpenClipboard(0)
        handle = d.user32.GetClipboardData(CF_UNICODETEXT)
        data = ctypes.c_wchar_p(handle).value
        d.user32.CloseClipboard()
        return data

    return copy_windows, paste_windows


copy, paste = init_windows_clipboard()
