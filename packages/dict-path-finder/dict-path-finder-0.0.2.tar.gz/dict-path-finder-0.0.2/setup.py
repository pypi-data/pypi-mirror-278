import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dict-path-finder",
    version="0.0.2",
    author="Jinhan Kim",
    author_email="developers.xyz@gmail.com",
    description="Find dictionary path by key and value",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/developers-dev/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)