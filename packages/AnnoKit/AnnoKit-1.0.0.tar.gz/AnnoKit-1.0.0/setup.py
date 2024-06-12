from setuptools import setup, find_packages
import re
import glob


classifiers = [
    "Development Status :: 3 - Alpha",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Information Analysis"
]

keywords = [
    'bioinformatics',
    'annotation file',
    'gtf',
    'gff'
]

def get_version():
    with open("annokit/__init__.py") as f:
        for line in f.readlines():
            m = re.match("__version__ = '([^']+)'", line)
            if m:
                return m.group(1)
        raise IOError("Version information can not found.")
    

def get_long_description():
    return "See https://github.com/iOLIGO/AnnoKit"

def get_install_requires():
    requirements = []
    with open('requirements.txt') as f:
        for line in f:
            requirements.append(line.strip())
    return requirements


setup(
    name='AnnoKit',
    author='cong wang',
    author_email='2119452560@qq.com',
    version=get_version(),
    license='MIT',
    description='annotation toolkit.',
    long_description=get_long_description(),
    keywords=keywords,
    url='https://github.com/iOLIGO/AnnoKit',
    packages=find_packages(),
    scripts=glob.glob('scripts/*'),
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    install_requires=get_install_requires(),
    python_requires='>=3.7, <4',
)