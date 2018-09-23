from setuptools import find_packages, setup

setup(
    name='memacs',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),  # Include all the python modules except `tests`.
)
