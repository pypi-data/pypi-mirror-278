from setuptools import find_packages, setup

setup(
    name='hTrackerIU',
    version='0.0.11',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'hTrackerIU=hTrackerIU.main:main',
        ],
    },
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'python-dateutil'
    ],
    extras_require={
        'dev': [
            'pytest',
            'httpx'
        ],
    },
    include_package_data=True,
    package_data={
        'hTrackerIU': [
            'static/*',
            'static/**/*',
            'static/**/**/*',
            'static/**/**/**/*'
        ],
    },
)
