from setuptools import setup, find_packages

setup(
    name='box_rest_api',
    version='1.0.0',
    description='A RESTful API',
    url='https://github.com/jebos/box_server',
    author='Jeremias Bosch',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
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

    keywords='rest restful api flask swagger flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.9.2', 'Flask-SQLAlchemy==2.1'],
)
