from setuptools import setup, find_packages

setup(
    name="ephys_analyzer",
    version="0.1.0",
    description="A GUI tool for analyzing electrophysiology data",
    author="Leonardo Garma",
    author_email="leonardogarma@gmail.com",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'matplotlib>=3.4.2',
        'pandas>=1.3.0',
        'openpyxl>=3.0.7',
        'intan_reader>=0.1.0',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ephys_analyzer=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)