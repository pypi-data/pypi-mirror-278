from importlib.metadata import version

from .magics import load_ipython_extension  # noqa: F401


__version__ = version("civis-jupyter-extensions")


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "static",
            "dest": "civis_jupyter_ext",
            "require": "civis_jupyter_ext/index",
        }
    ]
