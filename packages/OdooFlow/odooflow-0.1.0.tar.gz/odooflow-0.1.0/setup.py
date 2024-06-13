from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="OdooFlow",
    version="0.1.0",
    author="Fabian Anguiano",
    author_email="fabiananguiano@gmail.com",
    description="A package to create record's in Odoo simply and cleanly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tunahorse/OdooFlow",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "python-dotenv",
    ],
)
