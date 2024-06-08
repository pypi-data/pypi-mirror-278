import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()

VERSION = "0.1.36"
setuptools.setup(
    name='xango',
    version=VERSION,
    author='Mardix',
    author_email='mardix@blackdevhub.io',
    description='xango',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/mardix/xango',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    install_requires = [
        "cuid2",
        "arrow",
        "sqlglot",
        "pydash",
        "graphql-core",
        "python-slugify",
        "Jinja2 >= 3.0",
        "python-arango==7.5.8"
    ],
    packages=['xango'],
    package_dir={'':'src'}
)
