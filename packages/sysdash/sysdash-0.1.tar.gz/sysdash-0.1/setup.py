from setuptools import setup, find_packages

setup(
    name='sysdash',
    version='0.1',
    packages=find_packages(),
    description='System information utility',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Spandan Chavan',
    author_email='spandanchavan727477@gmail.com',
    url='https://github.com/Spandan7724/sysdash',
    install_requires=[
        'psutil',
        'GPUtil',
        'uptime',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'sysdash = sysdash.sysdash:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
