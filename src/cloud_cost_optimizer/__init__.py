from importlib.metadata import version

try:
    __version__ = version("cloud-cost-optimizer")
except Exception:
    __version__ = "unknown"