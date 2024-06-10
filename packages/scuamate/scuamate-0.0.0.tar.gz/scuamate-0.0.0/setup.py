import setuptools
import re

def readme():
    with open("README.md", 'r') as f:
        return f.read()

# version-handling code stolen from: https://stackoverflow.com/questions/
    #458550/standard-way-to-embed-version-into-python-package
VERSIONFILE="scuamate/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name='scuamate',
    # version num.: MAJOR.MINOR.PATCH
    version=verstr,
    author='CSIRO, Drew Ellison Terasaki Hart',
    author_email='Drew.TerasakiHart@csiro.au',
    description=('Some Cloud Utilities to Advance Monitoring of Animals '
                 'and Their Ecosystems: utilities to help run, maintain, '
                 'check, and back up the cloud infrastructure for '
                 'next-generation wildlife monitoring projects '
                 '(including SpaceCows and the National Koala '
                 'Monitoring Program)'),
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/NextGenEcologicalMonitoring/scuamate',
    # include the download URL, from the latest release on Github
    download_url=('https://github.com/NextGenEcologicalMonitoring/scuamate/archive/'
                  '%s.tar.gz') % verstr,
    include_package_data=True,
    # packages=setuptools.find_packages(),
    packages=['scuamate',
              'scuamate.az',
              'scuamate.gc',
              'scuamate.gsattrack',
             ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ],
    keywords=('wildlife biodiversity ecological monitoring citizen community science'),
    project_urls={
        'Source': 'https://github.com/NextGenEcologicalMonitoring/scuamate',
    },
    python_requires='>=3.9',
)
