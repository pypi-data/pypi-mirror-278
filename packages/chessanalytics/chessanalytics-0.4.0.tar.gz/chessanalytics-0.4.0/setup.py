from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="chessanalytics",
    author="lot022",
    version="0.4.0",
    license="MIT",
    keywords="chess",
    python_requires=">=3.7",
    url="https://github.com/lot022/chessanalytics",
    description="Simple library to analyse chess games from .png files containing games played on Lichess.org.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['scipy'],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
