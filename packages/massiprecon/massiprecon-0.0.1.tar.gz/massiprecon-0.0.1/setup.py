from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Generate csv or jsons with ip info'
LONG_DESCRIPTION = 'Given a list of ips massiprecon will find location and provider info etc and write them to a csv or json'

# Setting up
setup(
    name="massiprecon",
    version=VERSION,
    author="Witchdoctor (malectrica)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['massiprecon'],
    install_requires=['argparse'],
    keywords=['python', 'hack', 'osint', 'recon', 'data', 'api', 'ip'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
