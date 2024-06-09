from setuptools import setup, find_packages

setup(
    name='py_mono_bank_pay',
    version='0.0.3',
    description='A client library for Monobank merchant API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Grechka Konstantin',
    author_email='ytextsocks@gmail.com',
    url='https://github.com/ithekozub/py_mono_bank_pay',
    packages=find_packages(),
    install_requires=[
        'requests',
        'ecdsa'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
