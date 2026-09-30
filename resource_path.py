from pathlib import Path
import sys

def resource_path(*parts):
    """Return a path to a bundled/project resource."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base.joinpath(*parts))
