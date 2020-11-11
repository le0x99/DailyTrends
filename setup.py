from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=0.24.2", "numpy>=1.16.4", "requests>=2.22.0", "tqdm>=4.35.0"]

setup(
    name="DailyTrends",
    version="4.2",
    author="Leonard Vorbeck",
    author_email="leomxyy@googlemail.com",
    description="A package to receive full-range daily Google Trends data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/le0x99/DailyTrends/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
