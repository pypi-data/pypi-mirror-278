from setuptools import find_packages, setup

setup(
        name='libcde',
        package_dir={"":"src"},
        packages=find_packages(where="./src"),
        version='0.0.2',
        description='A library to work with CDE .dt application files.',
        author='BotchedRPR',
        install_requires=[],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        tests_suite='tests',
)
