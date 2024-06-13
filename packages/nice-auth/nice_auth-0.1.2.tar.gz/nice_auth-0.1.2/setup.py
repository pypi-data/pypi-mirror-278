from setuptools import setup, find_packages

setup(
    name="nice_auth",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
    ],
    author="RUNNERS",
    author_email="dev@runners.im",
    description="A Python library for NICE authentication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/python-nice-auth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
