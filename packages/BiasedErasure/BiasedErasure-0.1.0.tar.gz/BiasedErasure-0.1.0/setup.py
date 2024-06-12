from setuptools import setup

setup(
    name='BiasedErasure',
    version='0.1.0',
    author='Gefen Baranes and Pablo Bonilla',
    author_email='gefenbaranes123@gmail.com',
    packages=['BiasedErasure'],
    license='LICENSE',
    description='Simulate logical circuits with loss errors with efficient smart decoding',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy>=1.21',
        'networkx',
        'matplotlib',
        'stim>=1.11.0',
        'pymatching>=2.1.0',
    ],
)
