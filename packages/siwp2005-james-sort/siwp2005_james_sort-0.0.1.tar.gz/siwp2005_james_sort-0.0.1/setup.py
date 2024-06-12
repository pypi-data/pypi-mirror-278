from setuptools import setup

setup(
    name='siwp2005-james-sort',
    version='0.0.1',
    packages=['sort'],
    package_dir={'': 'src'},
    author='James Wilson Lie',
    author_email='jameswl00012@gmail.com',
    description='A collection of sorting algorithms',
    long_description=open('README.md').read(),
    url='https://github.com/JamesWilsonLie/siwp2005-james-sort',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='sorting algorithms',
    install_requires=[],
    tests_require=['unittest'],
    test_suite='tests',
)