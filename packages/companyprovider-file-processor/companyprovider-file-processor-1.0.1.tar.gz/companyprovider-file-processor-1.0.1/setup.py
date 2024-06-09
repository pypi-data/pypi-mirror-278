from setuptools import setup, find_packages
setup(
	name='companyprovider-file-processor',
	version='1.0.1',
	author='Marcelo Lacroix',
	author_email='mlacroix@tdsoft.com.br',
	description='',
	packages=find_packages(),
	entry_points={
        'console_scripts': ['script=script:main'],
    },
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
	long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)