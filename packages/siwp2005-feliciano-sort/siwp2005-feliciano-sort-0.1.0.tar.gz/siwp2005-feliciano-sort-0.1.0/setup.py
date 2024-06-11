from setuptools import setup, find_packages

setup(
    name='siwp2005-feliciano-sort',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    description='A collection of sorting algorithms',
    author='Feliciano',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/siwp2005-feliciano-sort',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
