from datasette import hookimpl
import base64
import imghdr
import jinja2

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
    image_type = imghdr.what(None, h=value)
    if image_type not in ("png", "jpeg", "gif"):
        return None
    # Render as a data-uri
    return jinja2.Markup(
        '<img src="data:image/{};base64,{}" alt="">'.format(
            image_type, base64.b64encode(value).decode("utf8")
        )
    )
