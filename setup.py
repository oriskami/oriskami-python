import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []

if sys.version_info < (2, 6):
    warnings.warn(
        'Python 2.5 is not supported by Ubivar. If you have any question,'
        'please file an issue on Github or contact us at support@ubivar.com.',
        DeprecationWarning)
    install_requires.append('requests >= 0.8.8, < 0.10.1')
    install_requires.append('ssl')
else:
    install_requires.append('requests >= 0.8.8')

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

# Don't import ubivar module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubivar'))

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')



setup(name='ubivar',
    cmdclass={'build_py': build_py},
    version='0.7',
    description='Ubivar python bindings',
    author='Ubivar',
    author_email='support@ubivar.com',
    url='http://github.com/ubivar/ubivar-python',
    packages=['ubivar','ubivar.test','ubivar.test.resources'],
    package_data={'ubivar': ['data/ca-certificates.crt']},
    install_requires=install_requires,
    test_suite='ubivar.test.all',
    tests_require=['unittest2', 'mock'],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.6",
        # "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        # "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ])
