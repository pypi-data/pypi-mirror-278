from setuptools import setup, find_packages

VERSION = '0.3.1'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="fortifysql",
    version=VERSION,
    author="Archie Hickmott",
    author_email="<25hickmar@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['sqlparse'],
    keywords=["sql", "security"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)