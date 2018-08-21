# datasette-render-images

[![PyPI](https://img.shields.io/pypi/v/datasette-render-images.svg)](https://pypi.org/project/datasette-render-images/)
[![Travis CI](https://travis-ci.com/simonw/datasette-render-images.svg?branch=master)](https://travis-ci.com/simonw/datasette-render-images)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-json-html/blob/master/LICENSE)

A Datasette plugin that renders binary blob images with data-uris, using the new `render_cell` plugin hook available in Datasette master - see [issue 352](https://github.com/simonw/datasette/issues/352) for details.

If a database row contains binary image data (PNG, GIF or JPEG), this plugin will detect that it is an image (using the [imghdr module](https://docs.python.org/3/library/imghdr.html) and render that cell using an `<img src="data:image/png;base64,...">` element.
