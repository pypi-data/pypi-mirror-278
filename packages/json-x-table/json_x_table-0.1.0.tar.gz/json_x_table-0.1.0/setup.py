from setuptools import find_packages, setup

VERSION = '0.1.0'
DESCRIPTION = 'Convert your json dump files with a certain format to HTML tables in a fast and efficient way'
LONG_DESCRIPTION = '''Convert your json dump files with a certain format to HTML tables in a fast and efficient way.\nYou may want to override the functions in order to match any format that you want, with specific customizable column values.'''

setup(
    name="json_x_table",
    version=VERSION,
    author="Sagar Dhande",
    author_email="dhandesagar78@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["jsoncomment", "pathlib"],
    keywords=['python3', 'Json_to_HTML'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
