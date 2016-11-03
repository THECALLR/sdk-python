from distutils.core import setup
import sys

setup(
    name='callr',
    version='2.0.1',
    author='Michael Jacquin, Dion MITCHELL',
    author_email='michael.jacquin@callr.com, dion.mitchell@callr.com',
    packages=['callr'],
    scripts=[],
    url='https://github.com/THECALLR/sdk-python',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    description='Python>=2.7, SDK for CALLR API',
)
