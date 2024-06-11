import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ms4",
    version="2.10.0",
    author="Ahmed",
    author_email="alhranyahmed@gmail.com",
    description="A simple library for many things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Psoidh/ms4",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "bs4",
        "requests",
        "uuid",
        "pycountry",
        "user_agent",
        "mnemonic",
    ],
)