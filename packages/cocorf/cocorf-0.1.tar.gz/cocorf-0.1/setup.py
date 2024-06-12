import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cocorf",
    version="0.1",
    author_email="Zxqinn@gmail.com",
    description="Comment-based codebase refining framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['torch==1.3.1','numpy','sklearn','nltk'], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)