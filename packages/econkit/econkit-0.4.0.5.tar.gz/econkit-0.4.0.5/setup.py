from setuptools import setup, find_packages
from econkit.version import __version__

setup(
    name='econkit',
    version=__version__,
    packages=find_packages(),
    description='Advanced Econometric Analysis Tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Stefanos Stavrianos',
    author_email='contact@stefanstavrianos.eu',
    url='https://www.stefanstavrianos.eu/',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'statsmodels',
        'yfinance',
        'requests',
        'matplotlib',
        'plotly'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
