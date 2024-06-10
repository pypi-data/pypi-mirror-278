from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scientometrics",  # Replace with your package name
    version="0.1.0",
    author="Abhirup Nandy, Nilabhra Rohan Das",
    author_email="abhirupnandy.rocks@gmail.com, nr.das@yahoo.com",
    description="A package for calculating scientometric indices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhirupnandy/scientometrics",
    project_urls={
        "Bug Tracker": "https://github.com/abhirupnandy/scientometrics/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "scientometrics"},
    packages=find_packages(where="scientometrics"),
    python_requires=">=3.6",
)
