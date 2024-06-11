from setuptools import setup

VERSION = '2.0.0'  # Updated version
DESCRIPTION = 'Open Redirect Bug Detection Tool'
LONG_DESCRIPTION = """
This tool is designed to detect and analyze open redirect vulnerabilities in web applications.
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openredirectscan",
    version=VERSION,
    author="@yuva",
    author_email="<yuvarajchandran93@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'openredirectscan = packages.main:main',
        ],
    },
    install_requires=['requests', 'argparse'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
