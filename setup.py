"""
A simple setup script to create an executable using PyQt5. This also
demonstrates the method for creating a Windows executable that does not have
an associated console.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""
import os
import shutil
from cx_Freeze import setup, Executable
#icon="icon.ico",base = "Win32GUI",
executables = [Executable("main.py",icon="icon.ico",target_name="PDF快速合併ツール",copyright="Copyright © 2022 MOTOYAMA. All rights reserved.",shortcut_name="PDF快速合併ツール")]

includefiles = ['icon.ico']
build_exe_options={
                    "optimize": 1,
                    "include_files":includefiles,
                    "silent_level":1,
                    'build_exe': 'Application/execute file'
                }


setup(
    name="PDF快速合併ツール",

    version="1.0",
    description="PDF快速合併ツール",
    long_description="2022/07 株式会社モトヤマ 設計",
    options = {"build_exe": build_exe_options},
    executables=executables,
)
