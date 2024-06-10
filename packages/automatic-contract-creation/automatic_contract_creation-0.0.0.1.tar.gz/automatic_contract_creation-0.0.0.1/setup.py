from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
	name="automatic_contract_creation",
	version="0.0.0.1",
	author="Mira Terekhova",
	author_email="miraterekhova@mail.ru",
	description="This is package designed for auto-generation of contracts and tests in the soda syntax",
	long_description=readme(),
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)
