
from setuptools import setup, find_packages

setup(
    name='thesisbot',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'experta',
        'scikit-learn',
        'flask',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for decision making using expert systems and text similarity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mylibrary',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
