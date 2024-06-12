from setuptools import setup, find_packages

setup(
	name="algebraic_hbm",
	version="0.1.1",
	author="Hannes Dänschel",
	author_email="daenschel@math.tu-berlin.de",
	description="Python implementation of the algebraic harmonic balance method for second order ordinary differential equations with polynomial coefficients.",
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url="https://git.tu-berlin.de/hannes.daenschel/algebraic-hbm",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10',
	install_requires=[
		'matplotlib',
		'numpy',
		'numba',
		'scipy'
	],
)