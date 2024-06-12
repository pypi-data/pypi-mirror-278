from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="aspotify",
    version="1.0.0",
    author="Joumaico Maulas",
    description="Asynchronous Spotify API Client",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/joumaico/aspotify",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=[
        "aspotify",
    ],
    package_dir={
        "aspotify": "src/aspotify",
    },
    python_requires=">=3.7",
    install_requires=[
        "aiohttp",
        "librespot",
        "redis",
    ],
)
