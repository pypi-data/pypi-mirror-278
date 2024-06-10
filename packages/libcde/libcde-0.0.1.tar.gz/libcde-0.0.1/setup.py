from setuptools import find_packages, setup

setup(
        name='libcde',
        packages=find_packages(include=['libcde']),
        version='0.0.1',
        description='A library to work with CDE .dt application files.',
        author='BotchedRPR',
        install_requires=[],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        tests_suite='tests',
)
