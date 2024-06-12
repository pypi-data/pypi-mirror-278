from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='fin_indicator',
    version='0.1.0',
    description='A library that calculates financial indicators and different signals resulting from Japanese candlestick patterns and indicators.',
    author='Marco Misseri',
    author_email='marco.misseri.monaco@gmail.com',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
