import codecs
import os
import re
import sys
import shutil

import setuptools

PACKAGE = 'granula'


def get_version():
    pattern = re.compile(r'__version__\s*=\s*(?P<version>\'\d+\.\d+\.\d+\')')
    with codecs.open('{}/__init__.py'.format(PACKAGE)) as f:
        match = pattern.search(f.read())
        if match is not None:
            return match.group('version')

        raise ValueError('Version not found for package "{}"'.format(PACKAGE))


def get_description():
    with codecs.open('README.rst', encoding='utf-8') as f:
        return '\n' + f.read()


def get_requirements():
    requirements = []

    with codecs.open('requirements.txt', encoding='utf-8') as f:
        for requirement in f:
            if '#' in requirement:
                requirement, _, _ = requirement.partition('#')

            requirement = requirement.strip()
            if requirement and not requirement.startswith('-r '):
                requirements.append(requirement)

    return requirements


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


class UploadCommand(setuptools.Command):
    """
    Support setup.py publish.
    """
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def _print_status(text):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(text))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self._print_status('Removing previous builds...')
        shutil.rmtree('dist', ignore_errors=True)

        self._print_status('Building source distribution...')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self._print_status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        self._print_status('Pushing git tags...')
        os.system('git tag v{0}'.format(get_version()))
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=PACKAGE,
    version=get_version(),
    description='Multi-file Configurations for Python Applications',
    long_description=get_description(),
    author='Vladislav Blinov',
    author_email='cunningplan@yandex.ru',
    url='https://github.com/chomechome/granula',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=get_requirements(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)