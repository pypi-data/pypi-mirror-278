from sphinx.application import Sphinx

from sphinx_nbblog.__about__ import __version__


def setup(app: Sphinx) -> dict:
    from sphinx_nbblog.extension import setup_extension

    setup_extension(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
