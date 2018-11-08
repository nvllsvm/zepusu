import setuptools

setuptools.setup(
    name='zepusu',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://gitlab.com/nvllsvm/zepusu',
    license='MIT',
    description='A minimalist ZeroMQ pub-sub command line client.',
    long_description=open('README.rst').read(),
    packages=['zepusu'],
    install_requires=['pyzmq'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    entry_points={'console_scripts': ['zepusu=zepusu:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6')
