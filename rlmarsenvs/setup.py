#
# Project: RL-self-driving-car
# Created by bbrighttaer on 
#


from setuptools import setup, find_packages

setup(
    name='rlmarsenvs',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['gym', 'pymunk >= 4.0', 'pygame', 'numpy'],
    url='',
    license='MIT',
    author='bbrighttaer',
    author_email='brighteragyemang@gmail.com',
    description='A collection of OpenAI Gym compatible RL environments'
)
