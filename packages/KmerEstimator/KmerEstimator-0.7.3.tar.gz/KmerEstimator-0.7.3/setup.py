from setuptools import setup, find_packages
setup(
	name='KmerEstimator',
	version='0.7.3',
	author='Srijan Chakraborty, Emily Liang, William Chu',
	description='A kmer estimator for genome assemblies',
        license='MIT',
	packages=find_packages(),
    install_requires = [
        'numpy',
        'matplotlib',
	'memory-profiler',
    ],
    
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
    
	python_requires='>=3.6',
	entry_points={
        	'console_scripts': [
            		'kmerestimator=kmerestimator.kmerestimator:main',
        	],
    },
)
