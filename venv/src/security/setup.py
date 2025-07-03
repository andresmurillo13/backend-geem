from setuptools import setup


install_requires = [
    'starlette==0.13.6',
    'meliodas==1.0.9',
    'rocketchat==1.0.0',
    'hawk==1.0.7'
]


test_require = [
    'ipython==7.16.1',
    'pytest==5.4.3',
    'pytest-asyncio==0.14.0',
    'pytest-cov==2.10.0',
    'nest-asyncio==1.3.0',
    'ujson==3.0.0'
]

setup(
    name='security',
    version='1.0.2',
    packages=['security'],
    install_requires=install_requires,
    author='Danilo Vargas',
    dependency_links=[
        'https://github.com/dasouch/meliodas.git@v1.0.9#egg=meliodas',
        'https://github.com/dasouch/rocketchat-singleton.git@v1.0.0#egg=rocketchat',
        'https://github.com/dasouch/hawk.git@v1.0.7#egg=hawk'
    ]
)
