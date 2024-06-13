from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
setup(
    name='record_temp_analysis_nc',
    version='0.1.3',
    description='A package to analyze and plot record-breaking temperatures.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Bijan Fallah',
    author_email='bijan.fallah@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'netCDF4',
        'matplotlib',
        'cartopy',
        'tqdm',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

