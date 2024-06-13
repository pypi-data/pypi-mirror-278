from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description_content = f.read()

description_content = "A Python library for managing state with synchronous or asynchronous side effects effortlessly."

setup(
    name="sideeffect",
    version="1.0.2",
    packages=find_packages(),
    install_requires = [
        # "numpy>=1.11.1"
    ],
    entry_points={
        "console_scripts": [
            # "script": "filename:function"
        ]
    },
    description=description_content,
    long_description=long_description_content,
    long_description_content_type="text/markdown",
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
