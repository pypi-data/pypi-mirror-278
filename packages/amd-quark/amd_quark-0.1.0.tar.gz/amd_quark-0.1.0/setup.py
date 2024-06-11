from setuptools import setup, find_packages

setup(
    name="amd-quark",
    version="0.1.0",
    author="Thiago Crepaldi",
    author_email="thiago@thiagocrepaldi.com",
    description="A quantization package for PyTorch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
