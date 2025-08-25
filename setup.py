from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dosint',
    version='3.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests', 'python-whois', 'termcolor', 'phonenumbers', 'setuptools',
        'pyyaml', 'tinydb', 'googlesearch-python', 'Pillow', 'exifread',
        'python-docx', 'pygments', 'python-magic', 'beautifulsoup4'
    ],
    entry_points={'console_scripts': ['dosint = dosint.cli:main']},
    author='Your Name',
    description='An intelligent OSINT, CTF, & Forensics Assistant.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
