# setup.py

from setuptools import setup, find_packages

setup(
    name='aclvl_permissions',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'djangorestframework>=3.0',
    ],
    include_package_data=True,
    license='MIT License',
    description='A custom Django permissions package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shahbazism/aclvl_permissions',
    author='Saeid shahbazi',
    author_email='saeidshahbazi@zohomail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
