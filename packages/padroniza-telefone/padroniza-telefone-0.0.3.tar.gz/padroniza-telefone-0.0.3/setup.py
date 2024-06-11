from setuptools import setup


install_requires = []

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='padroniza-telefone',
    version='0.0.3',
    license='MIT License',
    author='Tatianno Alves',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tferreiraalves@gmail.com',
    keywords='standardize phone E164',
    description=u'Standardizes phone to E164 standard',
    packages=['padroniza_telefone'],
)