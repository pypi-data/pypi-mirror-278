from setuptools import setup, find_packages

setup(
    name='bffl',
    version='0.2.0',
    author='Ken Seehart',
    author_email='ken@agi.green',
    description='A framework for structured bitfield processing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bffl',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "libcst",
    ],
)
