import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('version.txt') as f:
    version = f.read()


setuptools.setup(
    name="bot_station",
    version=version,
    author="Maxim Marashan",
    # author_email="ericjaychi@gmail.com",
    description="Bot Station SDK + Web App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/ericjaychi/sample-pypi-package",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
