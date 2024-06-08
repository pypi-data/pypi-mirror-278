from setuptools import setup, find_packages
setup(
	name='KmerEstimator',
	version='0.7.0',
	author='Srijan Chakraborty, Emily Liang, William Chu',
	description='A kmer estimator for genome assemblies',
    license='MIT',
	packages=find_packages(),
    install_requires = [
        'numpy',
        'matplotlib'
    ],
    
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
    
	python_requires='>=3.6',
)
