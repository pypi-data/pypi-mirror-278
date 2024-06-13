from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="credopay-paymentgateway",
    version="0.1",
    author="Credopay",
    author_email="support@credopay.com",
    description="A Python library for the CredoPay payment gateway.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["credopay", "paymentgateway"],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
