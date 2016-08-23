# -*- coding: utf-8 -*-
# !python3



def py2exe():
    from _version import __version__
    from distutils.core import setup
    import py2exe

    dist_dir = "../bin"

    setup(
        name="RespoTool",
        version=__version__,
        description="Outil de gestion de signalements de cartes pour le jeu Aaaah !",
        author="Jinai",
        author_email="jinai.extinction@gmail.com",
        url="http://www.extinction.fr/minijeux/",
        options={"py2exe": {"compressed": True,
                            "optimize": 2,
                            "bundle_files": 2,
                            "dist_dir": dist_dir,
                            "dll_excludes": ['msvcr71.dll', 'pywintypes34.dll'],
                            "excludes": ['doctest', 'unittest', 'xml', 'xmlrpc', 'difflib',
                                         'optparse', 'dis', 'bz2', 'bdb', 'ftplib', 'optparse', 'pdb', 'pydoc',
                                         'pyexpat', 'pywintypes', 'selectors', 'socketserver', 'win32api', 'win32con',
                                         '_bz2', '_hashlib', '_lzma', '_ssl', 'argparse', 'gettext', 'netbios', 'netrc',
                                         'pkgutil', 'plistlib', 'pprint', 'py_compile', 'runpy', 'ssl', 'textwrap',
                                         'win32wnet', 'zipfile', '_multiprocessing', '_osx_support',
                                         '_strptime', '_threading_local', 'lzma', 'gzip', 'glob', 'getopt', 'getpass',
                                         'hmac', 'webbrowser', 'urllib', 'threading', 'subprocess', 'operators',
                                         ],
                            }
                 },
        zipfile=None,
        windows=[{"script": "RespoTool.py",
        		  "icon_resources": [(0, "resources/respotool.ico")],
        		  }],
        data_files=[('resources', ['resources/respotool.ico'])]
    )


if __name__ == '__main__':
    py2exe()
