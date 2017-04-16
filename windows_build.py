from cx_Freeze import setup, Executable
import os, os.path, shutil, sys

upxFlag = False
if '-upx' in sys.argv:
    sys.argv.remove('-upx')
    upxFlag = True

dir = 'distrib/windows'

print('[[ Running Puzzle HD through cx_Freeze! ]]')
print('>> Destination directory: %s' % dir)

if 'build' not in sys.argv:
    sys.argv.append('build')

if os.path.isdir(dir): shutil.rmtree(dir)
os.makedirs(dir)

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
            'build_exe': dir,
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
if os.path.isfile(dir + '/upx.exe'):
    os.unlink(dir + '/w9xpopen.exe') # not needed

if upxFlag:
    if os.path.isfile('upx.exe'):
        print('>> Found UPX, using it to compress the executables!')
        files = os.listdir(dir)
        upx = []
        for f in files:
            if f.endswith('.exe') or f.endswith('.dll') or f.endswith('.pyd'):
                upx.append('"%s/%s"' % (dir,f))
        os.system('upx -9 ' + ' '.join(upx))
        print('>> Compression complete.')
    else:
        print('>> UPX not found, binaries can\'t be compressed.')
        print('>> In order to build Puzzle HD with UPX, place the upx.exe file into '\
              'this folder.')

if os.path.isdir(dir + '/Icons'): shutil.rmtree(dir + '/Icons')
if os.path.isdir(dir + '/nsmblib-0.5a'): shutil.rmtree(dir + '/nsmblib-0.5a')
shutil.copytree('Icons', dir + '/Icons')
if os.path.isdir('nsmblib-0.5a'): shutil.copytree('nsmblib-0.5a', dir + '/nsmblib-0.5a')

print('>> Puzzle HD has been frozen to %s!' % dir)
