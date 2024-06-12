from setuptools import setup, find_packages

setup(
    name="rnaernie",
    version="0.1.0",
    author="WANG Ning",
    author_email="wangning.roci@gmail.com",
    description="RNAErnie: A Transformer-based Model for RNA understanding and tasks.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CatIIIIIIII/RNAErnie2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
