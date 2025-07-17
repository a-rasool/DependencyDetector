# -----------------------------------------------------------------------------
# Dependency Detector Package
# -----------------------------------------------------------------------------
# This package provides tools for detecting dependencies.
from importlib.metadata import version, PackageNotFoundError
import importlib
import logging

# ---------------------------------------------------------------
# Version
# ------------------------------------------------------------------
try:
    __version__ = version("dependency_detector")
except PackageNotFoundError:
    __version__ = "0.1.0-dev"

# ------------------------------------------------------------------
# Package‑wide logger
# ------------------------------------------------------------------
logger = logging.getLogger("dependency_detector")
logger.addHandler(logging.NullHandler())

# ------------------------------------------------------------------
# Lazy re‑exports
# ------------------------------------------------------------------
def __getattr__(name: str):
    if name == "getSparkSession":
        return importlib.import_module(".sparkSession", __name__).getSparkSession
    if name == "readData":
        return importlib.import_module(".dataReader", __name__).readData
    if name == "BayesianNetworkDetector":
        return importlib.import_module(".BayesianNetworkDetector", __name__).BayesianNetworkDetector
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(globals().keys() | {
        "getSparkSession",
        "readData",
        "BayesianNetworkDetector"
    })

__all__ = [
    "BayesianNetworkDetector",
    "getSparkSession",
    "readData",
    "logger",
    "__version__",
]