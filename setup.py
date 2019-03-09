import pathlib

import setuptools

REPO = pathlib.Path(__file__).parent

setuptools.setup(
    name='zepusu',
    version='0.2.0',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://gitlab.com/nvllsvm/zepusu',
    license='MIT',
    description='A minimalist ZeroMQ pub-sub command line client.',
    long_description=REPO.joinpath('README.rst').read_text(),
    py_modules=['zepusu'],
    install_requires=['pyzmq'],
    extras_require={
        'test': ['pytest']
    },
    entry_points={'console_scripts': ['zepusu=zepusu:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6')
