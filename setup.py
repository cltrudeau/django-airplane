import os
from airplane import __version__

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()

SETUP_ARGS = dict(
    name='django-airplane',
    version=__version__,
    description=('Django app that caches CDN files for use when '
        'coding offline '),
    long_description=long_description,
    url='https://github.com/cltrudeau/django-airplane',
    author='Christopher Trudeau',
    author_email='ctrudeau+pypi@arsensa.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django,cache,offline,CDN,static',
    test_suite="load_tests.get_suite",
    install_requires=[
        'Django>=4.1',
        'requests>=2.23',
    ],
    tests_require=[
        'context_temp>=0.11.1',
        'django-awl>=0.24.0',
        'waelstow>=0.10.2',
    ]
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
