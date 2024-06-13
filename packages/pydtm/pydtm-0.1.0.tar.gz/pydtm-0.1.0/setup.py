from setuptools import setup, find_packages

setup(
    name='pydtm',
    version='0.1.0',
    description='A Python library for the IOM DTM API',
    author='Human Geomonitor',
    author_email= 'david.gerard.23@ucl.ac.uk',
    url='https://github.com/Human-Geomonitor/PyDTM',  # Replace with your actual URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests', 
        'pandas',
        'matplotlib',
        'numpy',
        'geopandas'

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)