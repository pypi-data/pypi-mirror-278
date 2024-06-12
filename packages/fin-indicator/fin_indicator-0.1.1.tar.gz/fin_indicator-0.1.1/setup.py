from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='fin_indicator',
    version='0.1.1',
    description='A library that calculates financial indicators and different signals resulting from Japanese candlestick patterns and indicators.',
    author='Marco Misseri',
    author_email='marco.misseri.monaco@gmail.com',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
# pypi-AgEIcHlwaS5vcmcCJGIyMTE2YWQ5LWRkMGItNDg0ZC04ZjcxLWRmM2U3Nzk2NGY5NgACKlszLCI1YjAwNzE3OS1jNGFmLTQwNDMtYmVhYi1kNWNjYWM2YzY1OGQiXQAABiDf2Xu42AKEj1izEiU_mzjyBNbsoKTrZX0ufSVmhTJPtg