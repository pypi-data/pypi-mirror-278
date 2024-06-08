from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'ESSL users management'
LONG_DESCRIPTION = 'Internal helper package for ESSL users management'
setup(
    name='espy_contact',
    version='2.0.14',
    packages=find_packages(),
    install_requires=[
        'bcrypt==4.1.2',
        'pytest==8.1.1',
        'pydantic==2.7.1',
        'sqlalchemy==2.0.29',
        'PyYAML==6.0.1'
        ],
    author='Femi Adigun',
    author_email='femi.adigun@myeverlasting.net',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    keywords=['fastapi','ESSL','ReachAI']
)