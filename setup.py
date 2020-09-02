import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py_derive_cmd-TODO-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.1",
    author="six-two",
    author_email="info@six-two.dev",
    description="Simplifies the usage of the python cmd module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/six-two/py_derive_cmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)