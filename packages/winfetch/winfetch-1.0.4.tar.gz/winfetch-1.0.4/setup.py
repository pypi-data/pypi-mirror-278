from setuptools import setup, find_packages

setup(
    name='winfetch',
    version='1.0.4',
    packages=find_packages(),
    author="gamerjamer43",
    author_email="gamerjamer43@protonmail.com",
    description="command: winfetch. i made this as a funny windows version of neofetch in like an hour.",
    long_description="may add coloring and some other shit, otherwise this package will probably not be updated much.\n\nupdate 4: added color indeed.",
    license="GNU GENERAL PUBLIC LICENSE V3",
    platforms="windows",
    entry_points={
        'console_scripts': [
            'winfetch = winfetch.__main__:main',
        ],
    },
)
