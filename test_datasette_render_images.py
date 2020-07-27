from datasette_render_images import render_cell
from datasette.app import Datasette
import jinja2
import pytest

GIF_1x1 = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01D\x00;"
PNG_1x1 = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU\x00\x00\x00\nIDATx\x9cc\xfa\x0f\x00\x01\x05\x01\x02\xcf\xa0.\xcd\x00\x00\x00\x00IEND\xaeB`\x82"
# https://github.com/python/cpython/blob/master/Lib/test/imghdrdata/python.jpg
JPEG = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xdb\x00C\x01\x03\x03\x03\x04\x03\x04\x08\x04\x04\x08\x10\x0b\t\x0b\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\xff\xc0\x00\x11\x08\x00\x10\x00\x10\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x16\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x04\x05\xff\xc4\x00$\x10\x00\x01\x04\x01\x04\x02\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x06\x05\x07\x08\x12\x13\x11"\x00\x14\t12\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\xff\xc4\x00#\x11\x00\x01\x02\x05\x03\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x11\x03\x04\x05\x06!\x00\x121\x15\x16a\x81\xe1\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\x14\xa6\xd2j\x1bs\xc1\xe6\x13\x12\xd4\x95\x1c\xf3\x11c\xe4%e\xbe\xbaZ\xeciE@\xb1\xe5 \xb2T\xa5\x1f\xd2\xca\xb8\xfa\xf2 \xab\x96=\x97l\x935\xe6\x9bw\xd7\xe6m\xa7\x17\x81\xa5W\x1c\x7f\x1c\xeaq\xe2K9\xd7\xe3"S\xf2\x1ai\xde\xd4qJ8\xb4\x82\xe8K\x89*qi\x1e\xcd-!;\xf1\xef\xb9\x1at\xac\xee\xa1Zu\x8e\xd5H\xace[\x85\x8b\x81\x85{!)\x98g\xa9k\x94\xb9IeO\xb9\xc8\x85)\x11K\x81*\xf0z\xd9\xf2<\x80~U\xbe\r\xf6b\xa1@\xcc\xe8\xe6\x9a=\\\xb7C\xb3\xd7zeX\xb1\xd9Q!\x88\xbfd\xb8\xd3\xf1\xc3h\x04)\xc0\xd0\xfe\xbb<\x02\xe0<T\x07\xb4\xbd\xd9{T\xe6\'\xfbn\xdf\x94`\x14\x82b\x13\x8d\xb8R\x98(7\x05\x89ry`\xe42\x89o\xc3\x82\x8e\xa7R\x8c\xea \x8d\xbex\x19\x1f\x07\xad\x7f\xff\xd9'


@pytest.mark.parametrize(
    "input,expected",
    [
        ("hello", None),
        (1, None),
        (True, None),
        (
            GIF_1x1,
            '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="">',
        ),
        # If it's a unicode string, not bytes, it is ignored:
        (GIF_1x1.decode("latin1"), None),
        # 1x1 transparent PNG:
        (
            PNG_1x1,
            '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGP6DwABBQECz6AuzQAAAABJRU5ErkJggg==" alt="">',
        ),
        (PNG_1x1.decode("latin1"), None),
        # Smallest possible JPEG, from https://github.com/mathiasbynens/small/
        (
            JPEG,
            '<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/wAARCAAQABADASIAAhEBAxEB/8QAFgABAQEAAAAAAAAAAAAAAAAABwQF/8QAJBAAAQQBBAICAwAAAAAAAAAAAQIDBAYFBwgSExEiABQJMTL/xAAVAQEBAAAAAAAAAAAAAAAAAAAABv/EACMRAAECBQMFAAAAAAAAAAAAAAECEQMEBQYhABIxFRZhgeH/2gAMAwEAAhEDEQA/ABSm0mobc8HmExLUlRzzEWPkJWW+ulrsaUVAseUgslSlH9LKuPryIKuWPZdskzXmm3fX5m2nF4GlVxx/HOpx4ks51+MiU/Iaad7UcUo4tILoS4kqcWkezS0hO/HvuRp0rO6hWnWO1UisZVuFi4GFeyEpmGepa5S5SWVPuciFKRFLgSrwetnyPIB+Vb4N9mKhQMzo5po9XLdDs9d6ZVix2VEhiL9kuNPxw2gEKcDQ/rs8AuA8VAe0vdl7VOYn+27flGAUgmITjbhSmCg3BYlyeWDkMolvw4KOp1KM6iCNvngZHwetf//Z" alt="">',
        ),
        (JPEG.decode("latin1"), None),
    ],
)
def test_render_cell(input, expected):
    actual = render_cell(input, None)
    assert expected == actual
    assert actual is None or isinstance(actual, jinja2.Markup)


def test_render_cell_maximum_image_size():
    max_length = 100 * 1024
    max_image = GIF_1x1 + (b"b" * (max_length - len(GIF_1x1)))
    rendered = render_cell(max_image, None)
    assert rendered is not None
    assert rendered.startswith("<img src")
    # Add one byte and it should no longer render
    assert None == render_cell(max_image + b"b", None)


def test_render_cell_different_size_limit():
    max_length = 100 * 1024
    max_image_plus_one = GIF_1x1 + (b"b" * (max_length - len(GIF_1x1))) + b"b"
    assert None == render_cell(max_image_plus_one, None)
    ds = Datasette(
        [],
        metadata={"plugins": {"datasette-render-images": {"size_limit": 101 * 1024}}},
    )
    rendered = render_cell(max_image_plus_one, ds)
    assert rendered is not None
    assert rendered.startswith("<img src")
