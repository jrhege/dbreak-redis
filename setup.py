from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dbreak-redis',
    version='0.0.1',
    py_modules=["dbreak_redis"],
    url='https://github.com/jrhege/dbreak_redis',
    author='Johnathon Hege',
    description='Plugin for dbreak to handle Redis connections',
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords="development database redis",
    python_requires='>=3.6',

    install_requires=[
        'dbreak>=0.0.1',
        'redis>=3.4.1'
    ],

    tests_require=[
        "fakeredis>=1.2.0",
        "pytest>=5.3.5"
    ],

    entry_points={
        "connection_wrappers": [
            "redis = dbreak_redis:RedisWrapper"
        ]
    }
)
