from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        raise RuntimeError("You are trying to install a stub package internal-big-query-client. Maybe you are using the wrong pypi?")


setup(
    name='internal-big-query-client',
    version='1.0.1',
    author='john.doe',
    author_email='john.doe.mayday2023@gmail.com',
    url='https://pypi.org/security/',
    readme="README.md",
    long_description="""This is a security placeholder package.""",
    long_description_content_type='text/markdown',
    description='A package to prevent Dependency Confusion attacks',
    cmdclass={
        'install': InstallCommand,
    },
)
