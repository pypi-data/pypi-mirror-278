from setuptools import setup 
import mxbt

VERSION = mxbt.__version__
DESCRIPTION = 'Yet another Matrix bot library.'

with open("README.md", "r") as ofile:
    LONG_DESCRIPTION = ofile.read()

packages = [
    'mxbt', 'mxbt.types'
]

# Setting up
setup(
    url="https://codeberg.org/librehub/mxbt",
    name="mxbt",
    version=VERSION,
    author="loliconshik3",
    author_email="loliconshik3@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=packages,
    install_requires=['matrix-nio', 'pillow', 'markdown', 'cryptography', 'filetype', 'aiofiles', 'python-dotenv'],
    keywords=['python', 'matrix-nio', 'matrix', 'bot', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
