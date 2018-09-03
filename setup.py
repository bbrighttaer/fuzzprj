from setuptools import setup

setup(
    name='fuzzprj',
    version='0.0.1',
    packages=['fuzzrl.fuzzrl', 'fuzzrl.fuzzrl.core', 'fuzzrl.fuzzrl.core.ga', 'fuzzrl.fuzzrl.core.io',
              'fuzzrl.fuzzrl.core.reg', 'fuzzrl.fuzzrl.core.res', 'fuzzrl.fuzzrl.core.conf',
              'fuzzrl.fuzzrl.core.plot', 'fuzzrl.fuzzrl.core.test', 'fuzzrl.fuzzrl.core.util',
              'fuzzrl.fuzzrl.core.fuzzy', 'fuzzrl.fuzzrl.core.algorithm', 'rlmarsenvs.tests',
              'rlmarsenvs.rlmarsenvs', 'rlmarsenvs.rlmarsenvs.envs'],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='Root folder of fuzzrl project', install_requires=['deap', 'numpy', 'scikit-fuzzy', 'gym',
                                                                     'matplotlib', 'networkx']
)
