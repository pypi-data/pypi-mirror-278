# setup.py

from setuptools import setup, find_packages

setup(
    name="sunny_order_splitter",
    version="0.2.3",
    packages=find_packages(),
    install_requires=["binance-connector","binance-futures-connector"],
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="glede",
    author_email="",
    url="https://github.com/sunnytrade/sunny-order-splitter-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
