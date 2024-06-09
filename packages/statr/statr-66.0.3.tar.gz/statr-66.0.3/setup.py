from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        raise RuntimeError("You are trying to install a stub package statr. Maybe you are using the wrong pypi? See https://nda.ya.ru/t/GljGihbC5zAGGz for details")


setup(
    name='statr',
    version='66.0.3',
    author='Yandex',
    author_email='security@yandex-team.ru',
    url='https://ya.ru',
    readme="README.md",
    long_description="""This is a security placeholder package.
If you want to claim this name for legitimate purposes,
please contact us at security@yandex-team.ru or pypi-security@yandex-team.ru""",
    long_description_content_type='text/markdown',
    description='A package to prevent Dependency Confusion attacks against Yandex.',
    cmdclass={
        'install': InstallCommand,
    },
)
