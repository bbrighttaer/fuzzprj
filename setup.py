# setup.py
from setuptools import setup,find_packages

# library setup
setup(
    name='fuzzrl',
    version='0.0.1',
    packages=[package for package in find_packages()
                if package.startswith('fuzzrl')],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='Library for GFT operations',
    install_requires=['numpy', 'deap', 'scikit-fuzzy', 'networkx']
)

# environments setup
setup(
    name='rlmarsenvs',
    version='0.0.1',
    packages=[package for package in find_packages()
                if package.startswith('rlmarsenvs')],
    install_requires=['gym', 'pymunk >= 4.0', 'pygame', 'numpy'],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='A collection of OpenAI Gym compatible RL environments'
)
