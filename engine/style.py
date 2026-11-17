"""Palette DOSSIER 00 lue depuis da/da.css (source unique de la DA)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DA_CSS = (ROOT / "da" / "da.css").read_text()


def _var(name: str, default: str) -> str:
    m = re.search(rf"--{name}:\s*(#[0-9a-fA-F]{{6}})", DA_CSS)
    return m.group(1) if m else default


PALETTE = {
    "charbon": _var("charbon", "#101113"),
    "archive": _var("archive", "#29292b"),
    "ivoire": _var("ivoire", "#e5ddcb"),
    "ambre": _var("ambre", "#d6a64a"),
    "rouge": _var("rouge", "#9e2929"),
}
# Silhouettes : noir charbon (palette stricte), détachées par un liseré ambre et les lumières du décor.
PALETTE["silhouette"] = PALETTE["charbon"]
