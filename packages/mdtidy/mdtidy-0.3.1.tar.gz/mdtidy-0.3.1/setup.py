from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mdtidy',
    version='0.3.1',
    description='A Python library to clean and format markdown content into Jupyter Notebooks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David Jeremiah',
    author_email='flasconnect@gmail.com',
    url='https://github.com/davidkjeremiah/mdtidy',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas'
    ]
)

