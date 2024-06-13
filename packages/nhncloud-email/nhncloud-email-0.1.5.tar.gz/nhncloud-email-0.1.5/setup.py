from setuptools import setup, find_packages

setup(
    name='nhncloud-email',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    description='A Python library to send Email using NHN Cloud API',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/python-nhncloud-email",
    author='RUNNERS',
    author_email="dev@runners.im",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
