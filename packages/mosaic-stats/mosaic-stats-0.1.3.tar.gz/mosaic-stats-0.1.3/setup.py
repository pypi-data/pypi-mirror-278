from setuptools import setup, find_packages

setup(
    name='mosaic-stats',
    version='0.1.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mosaic-stats=stats.stats:main',
        ],
    },
    install_requires=[
        'astropy',
        # Add other dependencies here if needed
    ],
    description='Statistics generation script for astrophotography mosaic projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Konstantin Dziuin',
    author_email='kdzuin@gmail.com',
    url='https://github.com/kdzuin/mosaic-stats',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)