from setuptools import setup, find_packages

version = '0.4'

setup(
    name='slc.clicktracker',
    version=version,
    description='Track user movements on your plone site.',
    long_description='\n'.join((
        open('README.txt').read(),
        open('HISTORY.txt').read(),
    )),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Plone',
    ],
    keywords='CMFEditions flexbox',
    author='Izak Burger, Syslab.com GmbH',
    author_email='isburger@gmail.com',
    url='https://github.com/syslabcom/slc.clicktracker',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['slc'],
    include_package_data=True,
    package_data={'slc.clicktracker': ['sql/*']},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'psycopg2 >=2.4.2',
        'plone.api',
    ],
    entry_points='''
        [z3c.autoinclude.plugin]
        target = plone
    ''',
)
