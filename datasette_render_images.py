from datasette import hookimpl
import base64
from markupsafe import Markup
from os import PathLike

DEFAULT_SIZE_LIMIT = 100 * 1024


@hookimpl
def render_cell(value, datasette):
    size_limit = DEFAULT_SIZE_LIMIT
    if datasette:
        plugin_config = datasette.plugin_config("datasette-render-images") or {}
        size_limit = plugin_config.get("size_limit") or DEFAULT_SIZE_LIMIT
    # Only act on byte columns
    if not isinstance(value, bytes):
        return None
    # Only render images < size_limit (default 100kb)
    if len(value) > size_limit:
        return None
    # Is this an image?
    image_type = what(None, h=value)
    if image_type not in ("png", "jpeg", "gif"):
        return None
    # Render as a data-uri
    return Markup(
        '<img src="data:image/{};base64,{}" alt="">'.format(
            image_type, base64.b64encode(value).decode("utf8")
        )
    )


# Below: vendored copy of imghdr since it will be removed in Python 3.13


def what(file, h=None):
    f = None
    try:
        if h is None:
            if isinstance(file, (str, PathLike)):
                f = open(file, "rb")
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f:
            f.close()
    return None


tests = []


def test_jpeg(h, f):
    """JPEG data with JFIF or Exif markers; and raw JPEG"""
    if h[6:10] in (b"JFIF", b"Exif"):
        return "jpeg"
    elif h[:4] == b"\xff\xd8\xff\xdb":
        return "jpeg"


tests.append(test_jpeg)


def test_png(h, f):
    if h.startswith(b"\211PNG\r\n\032\n"):
        return "png"


tests.append(test_png)


def test_gif(h, f):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"


tests.append(test_gif)


def test_tiff(h, f):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b"MM", b"II"):
        return "tiff"


tests.append(test_tiff)


def test_rgb(h, f):
    """SGI image library"""
    if h.startswith(b"\001\332"):
        return "rgb"


tests.append(test_rgb)


def test_pbm(h, f):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and h[0] == ord(b"P") and h[1] in b"14" and h[2] in b" \t\n\r":
        return "pbm"


tests.append(test_pbm)


def test_pgm(h, f):
    """PGM (portable graymap)"""
    if len(h) >= 3 and h[0] == ord(b"P") and h[1] in b"25" and h[2] in b" \t\n\r":
        return "pgm"


tests.append(test_pgm)


def test_ppm(h, f):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and h[0] == ord(b"P") and h[1] in b"36" and h[2] in b" \t\n\r":
        return "ppm"


tests.append(test_ppm)


def test_rast(h, f):
    """Sun raster file"""
    if h.startswith(b"\x59\xA6\x6A\x95"):
        return "rast"


tests.append(test_rast)


def test_xbm(h, f):
    """X bitmap (X10 or X11)"""
    if h.startswith(b"#define "):
        return "xbm"


tests.append(test_xbm)


def test_bmp(h, f):
    if h.startswith(b"BM"):
        return "bmp"


tests.append(test_bmp)


def test_webp(h, f):
    if h.startswith(b"RIFF") and h[8:12] == b"WEBP":
        return "webp"


tests.append(test_webp)


def test_exr(h, f):
    if h.startswith(b"\x76\x2f\x31\x01"):
        return "exr"


tests.append(test_exr)
