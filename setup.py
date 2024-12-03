from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('src/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Scytale exercise',
    version='0.1.0',
    description='A Scytale exercise for extract PL from git and convert to parquet',
    author='Yair Alon',
    author_email='kuyu12@gmail.com',
    url='https://github.com/yourusername/yourproject',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'etl=etl:main',
        ],
    },
)