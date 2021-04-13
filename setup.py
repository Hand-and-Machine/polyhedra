import os
from setuptools import setup, find_packages
from polyhedra import __version__

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='polyhedra',
    version=__version__,
    description='A Python package for manipulating 3D polyhedra.',
    author='Franklin Pezzuti Dyer',
    author_email='franklin+polyhedra@dyer.me',
    packages=find_packages(exclude=('docs', 'tests')),
    include_package_data=True,
    package_requires=[
        'numpy',
        'os'
    ]
    )
