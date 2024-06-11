from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="orcan",
    description="not the best reconnaissance tool, but it is a reconnaissance tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Erfan Samandarian",
    author_email="mail@erfansamandarian.com",
    url="https://erfansamandarian.com/soundbook",
    license="MIT",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["requests", "tabulate", "termcolor"],
    py_modules=["orcan"],
    entry_points={"console_scripts": ["orcan=orcan:main"]},
)
