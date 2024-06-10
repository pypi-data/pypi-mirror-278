from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'self-healing framework'
LONG_DESCRIPTION = 'A self-healing web driver that connects to an application and delivers reports for self-healing being done'

setup(
    name="qadapt",
    version=VERSION,
    author="IOTA_devs",
    author_email="a01571087@tec.mx",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['selenium', 'requests', 'pandas', 'scikit_learn'],
    keywords=['python', 'video', 'stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
