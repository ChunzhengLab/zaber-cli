from setuptools import setup

setup(
    name='zaber-cli',
    version='0.1.0',
    description='Command-line interface for controlling Zaber motion stages',
    author='Chunzheng Wang',
    author_email='wangcz22@m.fudan.edu.cn',
    scripts=['scripts/ZABER'],
    install_requires=[
        'pyserial',
        'rich'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.6',
)