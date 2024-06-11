from setuptools import setup, find_packages

setup(
    name="fillplace",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        "requests",
        "google-generativeai",
    ],
    author="Kunal Khairnar",
    author_email="kunalkhairnar2005@gmail.com",
    description="A package for generating meaningful placeholder content.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Kunal-Khairnar-05/fillplace",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)