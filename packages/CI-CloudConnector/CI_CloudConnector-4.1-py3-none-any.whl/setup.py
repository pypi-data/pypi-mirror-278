from setuptools import setup, find_packages

setup(
    name="CI_CloudConnector",
    version="4.1",
    packages=find_packages(),
    py_modules=["logic", "main", "setup", "myservice", "myservice_installer"],
    description="IOT application that collects data from PLC (ModBus or AnB Ethernet/IP) and sends it to the cloud using HTTPS",
    author="Yochai",
    author_email="",
    install_requires=[],
    url="https://trunovate.com/",
    long_description=open("README.txt").read()  # Make sure you have README.txt in the same directory
)