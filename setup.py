import setuptools


setuptools.setup(
    name='zepusu',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://gitlab.com/nvllsvm/zepusu',
    license='MIT',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    entry_points={
        'console_scripts': ['zepusu=zepusu:main']
    }
)
