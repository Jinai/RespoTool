# -*- mode: python -*-

import sys

sys.dont_write_bytecode = True
block_cipher = None

a = Analysis(
    ['RespoTool.py'],
    pathex=['../'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'doctest', 'unittest', 'xml', 'xmlrpc', 'difflib', 'optparse', 'dis', 'bz2',
        'bdb', 'ftplib', 'optparse', 'pdb', 'pydoc', 'pyexpat', 'pywintypes',
        'selectors', 'socketserver', 'win32api', 'win32con', '_bz2', '_hashlib',
        '_lzma', '_ssl', 'netbios', 'netrc', 'pkgutil', 'plistlib', 'pprint',
        'py_compile', 'runpy', 'ssl', 'win32wnet', 'zipfile', '_multiprocessing',
        '_osx_support', '_strptime', '_threading_local', 'lzma', 'gzip', 'getopt',
        'getpass', 'hmac', 'webbrowser', 'urllib', 'operators',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='RespoTool',
    debug=False,
    strip=False,
    upx=True,
    console=True,
    icon='data\\img\\respotool.ico'
)
