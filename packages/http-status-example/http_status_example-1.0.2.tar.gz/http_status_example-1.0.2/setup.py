from setuptools import setup, find_packages

long_description = open("README.md", "r").read()

setup(
    name="http_status_example",
    version="1.0.2",
    description="prints the HTTP status code of either the default url or the url provided by the user",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Russ Nastala",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["requests~=2.32"],
    python_requires="~=3.8",
)