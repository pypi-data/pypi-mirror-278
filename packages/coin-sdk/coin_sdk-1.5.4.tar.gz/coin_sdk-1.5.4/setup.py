"""
CLI for obtaining JWT access tokens using the PKCE flow
"""

import sys
if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')

from setuptools import find_packages, setup

dependencies = ['requests==2.31.0',
                'cryptography==42.0.8',
                'pyjwt==2.8.0',
                'colorama==0.4.6',
                'sseclient-py==1.8.0',
                'six==1.16.0']

from setuptools import setup

setup(
    name='coin_sdk',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['tests']),
    version="1.5.4",
    license='Apache-2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='SDKs for Vereninging COIN\'s apis',  # Give a short description about your library
    author='Vereniging COIN',  # Type in your name
    author_email='devops@coin.nl',  # Type in your E-Mail
    url='https://gitlab.com/verenigingcoin-public/coin-sdk-python',
    # Provide either the link to your github or to your website
    keywords=['COIN', 'Numberportability', 'TELECOM', 'SDK'],  # Keywords that define your package best
    install_requires=dependencies,
    tests_require=dependencies,
    python_requires='>=3.10',
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.10',
    ],
)
