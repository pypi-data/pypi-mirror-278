from setuptools import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Pyplaylist_spotify',
    version='0.0.1',
    description='It generally creates and trigger a function to add songs into you spotify playlist',
    author= 'Subhendu Adhikari',
    #url = 'https://github.com/Spidy20/PyMusic_Player',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['spotify_playlist','playlist_maker','playlist_creater'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9 ',
    py_modules=['Pyplaylist_spotify'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'beautifulsoup4',
       
    ]
)