from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup


setup(
    name='dila',
    version='0.1.1',
    description='Dila is a open source web-based translation platform for translators, content creators and developers.',
    author='Jakub Skiepko',
    author_email='it@socialwifi.com',
    url='https://github.com/socialwifi/dila',
    packages=find_packages(exclude=['tests']),
    install_requires=[str(ir.req) for ir in parse_requirements('base_requirements.txt', session=False)],
    entry_points={
        'console_scripts': [
            'dila = dila.frontend.cli:run',
        ],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
)
