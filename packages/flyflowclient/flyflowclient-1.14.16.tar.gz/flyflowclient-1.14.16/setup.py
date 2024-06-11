from setuptools import setup, find_packages

setup(
    name="flyflowclient",
    version="1.14.16",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    author="Carl Cortright",
    author_email="carl@flyflow.dev",
    description="A client library for the FlyFlow API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flyflow-devs/flyflow-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)