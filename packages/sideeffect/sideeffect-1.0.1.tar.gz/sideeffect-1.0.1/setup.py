from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="sideeffect",
    version="1.0.1",
    packages=find_packages(),
    install_requires = [
        # "numpy>=1.11.1"
    ],
    entry_points={
        "console_scripts": [
            # "script": "filename:function"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
