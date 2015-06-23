from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('monkey-stable.py', base=base, targetName = 'NocMonkeyV0_03.exe', icon = 'monkey.ico')
]

setup(name='NocMonkey',
      version = '0.03',
      description = 'Clipboard Manager for NOC',
      options = {"build_exe" : {"includes" : "atexit", "include_files" :"monkey-head.png","build_exe" : "exe/"}},
      executables = executables)
