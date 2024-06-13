from setuptools import setup, find_packages

def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="onetimeantispam",
    version="1.0",
    author="onetimedev",
    author_email="onetimedev@mail.ru",
    description="AntiSpam",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/onetimegithub",
    packages=find_packages(),
    install_requires=["aiohttp"]
)
