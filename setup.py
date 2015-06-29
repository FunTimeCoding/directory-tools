try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='directory-tools',
    version='0.1',
    description='Stub description for directory-tools.',
    install_requires=[],
    scripts=['bin/dt'],
    packages=['directory_tools'],
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    url='http://example.org',
    download_url='http://example.org/directory-tools.tar.gz'
)
