from setuptools import setup
import re
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setup(
    version=find_version("functionalmodelservice", "__init__.py"),
    name='functionalmodelservice',
    description='a flask app for tracking metadata about different modeled responses to stimuli',
    author='Forrest Collman',
    author_email='forrestc@alleninstitute.org',
    url='https://github.com/AllenInstitute/FunctionalModelService',
    packages=['functionalmodelservice'],
    include_package_data=True,
    install_requires=required
)
