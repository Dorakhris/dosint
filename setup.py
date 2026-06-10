from setuptools import setup, find_packages
setup(
    name='dosint', version='3.2.0', package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests', 'python-whois', 'termcolor', 'phonenumbers', 'setuptools',
        'pyyaml', 'tinydb', 'googlesearch-python', 'Pillow', 'exifread',
        'python-docx', 'pygments', 'python-magic', 'beautifulsoup4', 'ddgs'
    ],
    entry_points={'console_scripts': ['dosint = dosint.cli:main']}
)
