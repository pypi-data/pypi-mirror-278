# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="xqueue",
    version="0.0.1",
    description="A distributed messaging library similar to rq built on top of Redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chishui/xq",
    author="chishui",
    author_email="chishui2@gmail.com",
    packages=find_packages(
        include=[
        "xq"
        ]),  # Required
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="rq,queue,redis,messaging",
    python_requires=">=3.8, <4",
)
