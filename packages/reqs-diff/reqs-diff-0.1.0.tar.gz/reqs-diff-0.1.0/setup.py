from setuptools import setup, find_packages

setup(
    name="reqs-diff",
    version="0.1.0",
    author="Brice Fotzo",
    author_email="bricef.tech@gmail.com",
    description="A tool to compare multiple requirements.txt files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bricefotzo/reqs-diff",
    packages=find_packages(),
    install_requires=["pandas", "tabulate", "termcolor"],
    entry_points={
        "console_scripts": [
            "reqs-diff=reqs_diff.compare:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
