# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-02-15 14:05:16
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-02-15 15:26:25
@FilePath: /simple_encryption/setup.py
@Description:
'''
import os
import sysconfig
from setuptools import setup,find_packages
from Cython.Build import build_ext, cythonize
from setuptools.command.build_py import build_py as _build_py

EXCLUDE_FILES = [
    'simecy/__init__.py',
    'simecy/__main__.py'
]


def get_ext_paths(root_dir, exclude_files):
    """get filepaths for compilation"""
    paths = []

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if os.path.splitext(filename)[1] not in ('.py',".pyx"):
                continue

            file_path = os.path.join(root, filename)
            if file_path in exclude_files:
                continue

            paths.append(file_path)
    return paths


class build_py(_build_py):

    def find_package_modules(self, package, package_dir):
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        modules = super().find_package_modules(package, package_dir)
        filtered_modules = []
        for (pkg, mod, filepath) in modules:
            if os.path.exists(filepath.replace('.py', ext_suffix)):
                continue
            filtered_modules.append((pkg, mod, filepath, ))
        return filtered_modules
setup(
        name="simecy",
        version='0.4',
        description='simple encrypt file',
        author='captainfffsama',
        author_email='tuanzhangsama@outlook.com',
        packages=find_packages(),
        include_package_data=True,
        exclude_package_data ={"simecy":["*.c"]},
        license='MIT License',
        cmdclass={'build_py': build_py},
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        install_requires=['cryptography',],
        zip_safe=False,
        ext_modules=cythonize(get_ext_paths('simecy', EXCLUDE_FILES),language_level=3)
)
