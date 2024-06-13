from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="pypartpicker2",
    version="0.1.6",
    description="A package that scrapes pcpartpicker.com and returns the results as objects.",
    packages=["pypartpicker"],
    url="https://github.com/giuseppe99barchetta/pypartpicker",
    keywords=["pcpartpicker", "scraper", "list", "beautifulsoup", "pc", "parts"],
    install_requires=["bs4", "requests"],
    zip_safe=False,
    download_url="https://github.com/giuseppe99barchetta/pypartpicker/archive/refs/tags/0.1.6.tar.gz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
