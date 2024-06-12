from setuptools import setup, find_packages

setup(
    name='swollen',
    version='0.0.1',
    author='FedirT',
    author_email='ftymoshchuk@gmail.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ftymoshchuk',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)