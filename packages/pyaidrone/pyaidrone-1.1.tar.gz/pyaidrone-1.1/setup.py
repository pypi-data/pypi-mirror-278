from setuptools import setup, find_packages

setup(
    name = "pyaidrone",
    version = "1.1", 
    description = "Library for AIDrone Products",
    author = "IR-Brain",
    author_email = "ceo@ir-brain.com",
    url = "http://www.ir-brain.com",
    packages = ['pyaidrone', 
        ],
    install_requires = [
        'pyserial>=3.4',
        'pynput>=1.7.3',
        ],
)
