#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable
import os, os.path, shutil, sys

dir_ = 'distrib/puzzlehd'

print('[[ Running Puzzle HD through cx_Freeze! ]]')
print('>> Destination directory: %s' % dir_)

if 'build' not in sys.argv:
    sys.argv.append('build')

if os.path.isdir(dir_): shutil.rmtree(dir_)
os.makedirs(dir_)

# exclude QtWebKit to save space, plus Python stuff we don't use
excludes = ['doctest', 'pdb', 'unittest', 'difflib', 'inspect',
    'os2emxpath', 'posixpath', 'optpath', 'locale', 'calendar',
    'select', 'multiprocessing', 'ssl',
    'PyQt5.QtWebKit', 'PyQt5.QtNetwork']

# set it up
base = 'Win32GUI' if sys.platform == 'win32' else None
setup(
    name='Puzzle HD',
    version='1.0',
    description='Puzzle HD - New Super Mario Bros. U Tileset Editor',
    options={
        'build_exe': {
            'excludes': excludes,
            'packages': ['sip', 'encodings', 'encodings.hex_codec', 'encodings.utf_8'],
            'compressed': 1,
            'build_exe': dir_,
            },
        },
    executables = [
        Executable(
            'puzzlehd.py',
            base = base,
            ),
        ],
    )

print('>> Built frozen executable!')

# now that it's built, configure everything
if os.path.isfile(dir_ + '/upx.exe'):
    os.unlink(dir_ + '/w9xpopen.exe') # not needed

if os.path.isdir(dir_ + '/Icons'): shutil.rmtree(dir_ + '/Icons')
if os.path.isdir(dir_ + '/nsmblib-0.5a'): shutil.rmtree(dir_ + '/nsmblib-0.5a')
shutil.copytree('Icons', dir_ + '/Icons')
if os.path.isdir('nsmblib-0.5a'): shutil.copytree('nsmblib-0.5a', dir_ + '/nsmblib-0.5a')

print('>> Puzzle HD has been frozen to %s!' % dir_)
