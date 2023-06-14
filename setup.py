from setuptools import setup
import os

VERSION = "0.4"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-render-images",
    description="Datasette plugin that renders binary blob images using data-uris",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-render-images",
    license="Apache License, Version 2.0",
    version=VERSION,
    py_modules=["datasette_render_images"],
    entry_points={"datasette": ["render_images = datasette_render_images"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest"]},
    tests_require=["datasette-auth-tokens[test]"],
)
