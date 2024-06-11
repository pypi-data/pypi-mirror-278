from setuptools import setup

setup(
    name='bohr',
    version='0.2.72',
    author='DanC',
    author_email='dan.cabrol@bohr-energie.fr',
    packages=['bohr'],
    install_requires=[
        'psycopg2-binary==2.9.5',
        'pandas==2.0.1'
    ],
)