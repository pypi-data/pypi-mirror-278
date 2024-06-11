from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A module for create telegram bot easy'

setup(
    name="ptb-easy-bot",
    version=VERSION,
    author="Pamod Madubahana",
    author_email="premiumqtrst@gmail.com",
    packages=find_packages(),
    install_requires=['python-telegram-bot', 'python-telegram-bot[webhooks]'],
    keywords=['python', 'telegram bot', 'Easy Bots'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
