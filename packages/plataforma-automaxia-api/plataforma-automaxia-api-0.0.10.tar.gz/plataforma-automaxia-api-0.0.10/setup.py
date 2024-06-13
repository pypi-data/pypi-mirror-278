from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='plataforma-automaxia-api',
    version='0.0.10',
    license='MIT License',
    author='Wesley Romualdo da Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='wesleyromualdo@gmail.com',
    keywords='plataforma automaxia api',
    description=u'Wrapper oficial da Plataforma Automaxia para Python',
    packages=['plataforma'],
    install_requires=['requests'],)
