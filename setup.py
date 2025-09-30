from setuptools import setup, find_packages

setup(
    name="pycalypso",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[],
    author="Game_K",
    author_email="game_k@laposte.net",
    description="Custom Python library for web scraping, flexible and tailored to your projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Game-K-Hack/calypso",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
