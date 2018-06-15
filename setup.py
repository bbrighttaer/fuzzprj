from setuptools import setup

setup(
    name='fuzzprj',
    version='0.0.1',
    packages=['fuzznnrl.fuzznnrl', 'fuzznnrl.fuzznnrl.core', 'fuzznnrl.fuzznnrl.core.ga', 'fuzznnrl.fuzznnrl.core.io',
              'fuzznnrl.fuzznnrl.core.reg', 'fuzznnrl.fuzznnrl.core.res', 'fuzznnrl.fuzznnrl.core.conf',
              'fuzznnrl.fuzznnrl.core.plot', 'fuzznnrl.fuzznnrl.core.test', 'fuzznnrl.fuzznnrl.core.util',
              'fuzznnrl.fuzznnrl.core.fuzzy', 'fuzznnrl.fuzznnrl.core.algorithm', 'rlmarsenvs.tests',
              'rlmarsenvs.rlmarsenvs', 'rlmarsenvs.rlmarsenvs.envs'],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='Root folder of fuzznnrl project'
)
