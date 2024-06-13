from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from .del_marker import DelMarkerDirective

__version__ = '0.0.1'


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("del", DelMarkerDirective)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
