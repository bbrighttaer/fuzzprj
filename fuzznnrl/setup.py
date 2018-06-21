from setuptools import setup

setup(
    name='fuzznnrl',
    version='0.0.1',
    packages=['fuzznnrl', 'fuzznnrl.core', 'fuzznnrl.core.ga', 'fuzznnrl.core.io', 'fuzznnrl.core.reg',
              'fuzznnrl.core.res', 'fuzznnrl.core.conf', 'fuzznnrl.core.plot', 'fuzznnrl.core.test',
              'fuzznnrl.core.util', 'fuzznnrl.core.fuzzy', 'fuzznnrl.core.algorithm'],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='Library for GFT operations',
    install_requires=['numpy', 'deap', 'scikit-fuzzy', 'networkx']
)
