from setuptools import setup, find_packages

setup(
    name='stream-data-processing',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'psycopg2-binary',
        'kafka-python',
        'faker',
        'pyflink',
        'pyyaml',
        'python-dotenv'
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8'
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Stream Data Processing Project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/stream-data-processing',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)