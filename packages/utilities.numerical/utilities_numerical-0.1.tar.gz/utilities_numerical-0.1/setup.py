from setuptools import find_packages, setup

setup(
    name='utilities.numerical',
    version='0.1',
    packages=find_packages(include=['utilities', 'utilities.*']),
    # namespace_packages=['utilities'],
)
