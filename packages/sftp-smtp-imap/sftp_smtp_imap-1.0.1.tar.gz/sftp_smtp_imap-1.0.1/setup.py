from setuptools import setup, find_packages

with open('README.md',encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE.txt', encoding="utf-8") as f:
    license = f.read()

setup(
name='sftp_smtp_imap',
version='1.0.1',
author='Sunesh Pandita',
author_email='suneshpandita2009@gmail.com',
description='This package includes functionality to work with any SFTP, IMAP and SMTP server',
packages=find_packages(),
long_description=readme,
long_description_content_type="text/markdown",
license=license,
url="https://github.com/SUNESHPANDITA/sftp-smtp-imap-package.git",

platforms=["Windows"],
python_requires='>=3.10.0'
)