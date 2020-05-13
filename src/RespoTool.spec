# -*- mode: python -*-

block_cipher = None

added_files = [
    ("data/contact.json", "data"),
    ("data/duplicates_msg.json", "data"),
    ("data/respomaps.json", "data"),
    ("data/statuses.json", "data"),
    ("data/tags.json", "data"),
    ("data/img/respotool.ico", "data/img"),
    ("data/img/search1.png", "data/img"),
    ("data/img/search2.png", "data/img"),
    ("data/img/shield_respo.png", "data/img")
]

a = Analysis(
    ["RespoTool.py"],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "doctest", "unittest", "xml", "xmlrpc", "difflib", "optparse", "bz2",
        "bdb", "ftplib", "optparse", "pdb", "pydoc", "pyexpat", "pywintypes",
        "socketserver", "win32api", "win32con", "_bz2", "_hashlib",
        "_lzma", "_ssl", "netbios", "netrc", "pkgutil", "plistlib", "pprint",
        "py_compile", "runpy", "ssl", "win32wnet", "zipfile", "_multiprocessing",
        "_osx_support", "_strptime", "_threading_local", "lzma", "gzip", "getopt",
        "getpass", "hmac", "urllib", "operators"
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
    name="RespoTool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,
    icon="data\\img\\respotool.ico"
)
