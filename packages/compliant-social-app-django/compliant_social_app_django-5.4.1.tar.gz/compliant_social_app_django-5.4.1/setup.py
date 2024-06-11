"""Setup file for easy installation"""

import re
from os.path import dirname, join

from setuptools import setup

VERSION_RE = re.compile(r'__version__ = ["\']([\d\.]+)["\']')


def read_version():
    with open("compliant_social_django/__init__.py") as file:
        version_line = [
            line for line in file.readlines() if line.startswith("__version__")
        ][0]
        return VERSION_RE.match(version_line).groups()[0]


def long_description():
    return open(join(dirname(__file__), "README.md")).read()


def load_requirements():
    return open(join(dirname(__file__), "requirements.txt")).readlines()


setup(
    name="compliant-social-app-django",
    version=read_version(),
    author="Rightly",
    author_email="",
    description="Python Social Authentication, Django integration, Google compliant fork",
    license="BSD",
    keywords="django, social auth",
    url="https://github.com/RightlyGroup/compliant-social-app-django",
    packages=[
        "compliant_social_django",
        "compliant_social_django.audit",
        "compliant_social_django.backends",
        "compliant_social_django.migrations",
        "compliant_social_django.management",
        "compliant_social_django.management.commands",
        "compliant_social_django.pipeline",
    ],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=load_requirements(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    zip_safe=False,
)
