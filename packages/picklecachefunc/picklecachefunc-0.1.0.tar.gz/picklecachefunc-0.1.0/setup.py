from setuptools import setup, find_packages

setup(
    name='picklecachefunc',
    version='0.1.0',
    description='A decorator to cache function outputs to files using pickle.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/coallaoh/picklecachefunc',  # Replace with your GitHub URL
    author='Seong Joon Oh',
    author_email='coallaoh@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
