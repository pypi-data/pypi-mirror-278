"""Entrypoint for Jupyter kernels submited via WLMs,
such as SLURM or PBS Pro"""

from .ipykernel_wlm import main as ipykernel_wlm  # noqa

try:
    from ._version import __version__, __version_tuple__  # noqa
except ImportError:
    __version__ = "0.0.dev"

__author__ = "Bright Computing Holding BV"
__url__ = "http://brightcomputing.com"
