from datetime import datetime, timezone
from importlib.metadata import metadata, version as get_version

import cj365.flatdict

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
]

project = distribution_name = cj365.flatdict.__dist_name__
version = get_version(distribution_name)
release = f"v{version}"

meta = metadata(distribution_name)
maintainer_name = meta["Maintainer-email"].split("<", maxsplit=1)[0].strip()
current_year = datetime.now(tz=timezone.utc).astimezone().year
copyright = f"{current_year}, {maintainer_name}"

html_theme = "furo"
master_doc = "index"
exclude_patterns = ["_build"]
pygments_style = "sphinx"
source_suffix = ".rst"
templates_path = ["source/_templates"]
