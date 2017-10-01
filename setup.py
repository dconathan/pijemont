from distutils.core import setup

setup(
    name='pijemont',
    author='Daniel Ross',
    maintainer='Devin Conathan',
    version='0.2.0',
    packages=['pijemont'],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'ply==3.10',
        'PyYAML==3.12',
    ],
)
