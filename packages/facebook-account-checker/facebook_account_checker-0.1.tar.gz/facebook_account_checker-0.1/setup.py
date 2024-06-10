from setuptools import setup, find_packages

setup(
    name='facebook_account_checker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='ZexusDigital',
    author_email='zexusdigital@zexusdigital.com',
    description='A simple library to check Facebook accounts using Facebook API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZexusDigital/facebook_account_checker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
