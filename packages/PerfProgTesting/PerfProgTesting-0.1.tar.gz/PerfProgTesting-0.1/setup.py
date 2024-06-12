from setuptools import find_packages, setup

setup(
    name='PerfProgTesting',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'sqlparse>=0.4.1',
        'bootstrap4',  # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'manage.py = manage:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Operating System :: OS Independent',
    ],
)
