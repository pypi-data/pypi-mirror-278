import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-itbill>`_.
"""

version_path = 'uw_itbill/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='UW-RestClients-ITBill',
    version=VERSION,
    packages=['uw_itbill'],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=['UW-RestClients-Core<2.0',
                      'mock',
                     ],
    license='Apache License, Version 2.0',
    description=('A library for connecting to UW IT-Bill API'),
    long_description=README,
    url='https://github.com/uw-it-aca/uw-restclients-itbill',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
