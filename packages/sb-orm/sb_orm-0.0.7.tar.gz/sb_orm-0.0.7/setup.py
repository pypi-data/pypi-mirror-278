from setuptools import setup, find_packages

setup(
    name='sb-orm',
    version='0.0.4',
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
