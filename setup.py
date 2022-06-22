from setuptools import setup, find_packages


setup(
    name='mlx.treemap',
    use_scm_version={
        'write_to': 'mlx/__treemap_version__.py'
    },
    setup_requires=['setuptools-scm>=6.0.0,<7.*'],
    url='https://github.com/melexis/treemap',
    license='Apache License, Version 2.0',
    author='Jasper Craeghs',
    author_email='jce@melexis.com',
    description='Sphinx extension to generate a treemap of Cobertura data',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests', 'doc']),
    install_requires=['plotly', 'kaleido', 'pandas'],
    python_requires='>=3.6',
    namespace_packages=['mlx'],
    keywords=[
        'cobertura',
        'treemap',
        'test coverage',
        'visualization',
        'sphinx',
    ],
)
