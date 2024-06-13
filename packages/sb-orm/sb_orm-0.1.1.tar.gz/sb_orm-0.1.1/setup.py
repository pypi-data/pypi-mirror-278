from setuptools import setup, find_packages

setup(
    name='sb_orm',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'aiohttp',
        'pymysql'
    ],
    description='A python stupid mysql orm',
    author='idcim',
    author_email='rogermmg@gmail.com',
    url='https://github.com/idcim/sb_orm',
)
