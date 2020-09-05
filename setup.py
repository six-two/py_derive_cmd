import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

PACKAGE = "py_derive_cmd"

setuptools.setup(
    name=PACKAGE, # py_derive_cmd-TODO-YOUR-USERNAME-HERE
    version="0.0.1",
    author="six-two",
    author_email="info@six-two.dev",
    description="Simplifies the usage of the python cmd module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/six-two/py_derive_cmd",
    packages=[PACKAGE],
    package_data={PACKAGE: ["py.typed"]},
    zip_save=False,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)