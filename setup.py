#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='directory-tools',
    version='0.1.0',
    description='Manage OpenLDAP users and groups.',
    url='https://github.com/FunTimeCoding/directory-tools',
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: System :: Systems Administration :: Authentication/Directory'
        ' :: LDAP',
    ],
    keywords='slapd openldap abstraction command line web service',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyyaml', 'flask', 'ldap3'],
    python_requires='>=3.2',
    entry_points={
        'console_scripts': [
            'dt=directory_tools.directory_tools:'
            'DirectoryTools.main',
        ],
    },
)
