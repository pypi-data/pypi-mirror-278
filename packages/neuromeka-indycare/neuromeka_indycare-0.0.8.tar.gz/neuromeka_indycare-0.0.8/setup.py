from setuptools import setup, find_packages
import os
import shutil

setup(
    name='neuromeka_indycare',
    version='0.0.8',
    description='Neuromeka IndyCare Package',
    author='Neuromeka',
    author_email='ilhyeok.kwon@neuromeka.com',
    url='https://gitlab.com/neuromeka-group/nrmkf/indycarereporter_v3',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'multiprocess',
        'pyyaml',
        'neuromeka==3.2.0.2',
        'paho-mqtt==1.6.1',
        'opencv-python',
        'pyngrok==5.1.0'
    ],
    entry_points={
        'console_scripts': [
            'setup_indycare=neuromeka_indycare.setup_param:main',
            'run_indycare=neuromeka_indycare.IndyCAREReport:main'
        ]
    },
    include_package_data=True,
    package_data={
            'neuromeka_indycare': [
            'indycare_utils/config.yml',
            'indycare_utils/*.py',
            'daliworks_software/*',
            'setup/*',
            'IndyCAREReport.py',
            'setup_param.py',
            'create_service.sh'
        ],
    },
)
