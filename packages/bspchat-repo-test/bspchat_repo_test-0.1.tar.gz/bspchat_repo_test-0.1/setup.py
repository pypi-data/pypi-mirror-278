from setuptools import setup, find_packages

setup(
    name='bspchat_repo_test',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'boto3==1.24.28'
    ],
    description='Utilidades de prueba',
    author='Kenny Mendieta',
    author_email='kenny.mendieta@bspchat.com'
)
