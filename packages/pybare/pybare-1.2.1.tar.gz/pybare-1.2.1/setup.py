import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybare",  # Replace with your own username
    version="1.2.1",
    author="Noah Pederson",
    author_email="noah@packetlost.dev",
    description="A declarative implementation of BARE for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sr.ht/~chiefnoah/pybare/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
