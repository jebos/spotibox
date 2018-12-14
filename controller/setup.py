from setuptools import setup, find_packages

setup(
    name='spotibox',
    version='1.0.0',
    description='A spotify python client reading rfid cards and calling spotify webapi to play a song',
    url='https://github.com/jebos/box',
    author='Jeremias Bosch',

    classifiers=[
        'Development Status :: ',
        'Intended Audience :: ',
        'Topic :: Libraries :: Application Frameworks',
        'License :: GLPv2',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='spotipy',

    packages=find_packages(),

    install_requires=['spotipy'],
)
