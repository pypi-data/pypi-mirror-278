from setuptools import setup, find_packages

setup(
    name='record_temp_analysis_nc',
    version='0.1.1',
    description='A package to analyze and plot record-breaking temperatures.',
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

