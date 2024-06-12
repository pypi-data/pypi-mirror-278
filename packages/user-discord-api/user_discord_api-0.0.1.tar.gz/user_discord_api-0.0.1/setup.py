from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Allows you to use discord tokens for messages'
LONG_DESCRIPTION = 'Discord python for User Tokens allows messages, tokeninfo and token login.'

# Setting up
setup(
    name="user_discord_api",
    version=VERSION,
    author="tntgamer1337",
    author_email="<tntgamer133701@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'selenium'],
    keywords=['python', 'discord', 'user', 'api', 'package', 'easy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)