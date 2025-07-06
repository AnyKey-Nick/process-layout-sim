import yaml
from pathlib import Path


def load_layout(path: str | Path) -> dict:
    """Load layout configuration from YAML."""
    with open(path, 'r', encoding='utf-8') as fh:
        data = yaml.safe_load(fh)
    return data.get('layout', {})


def save_layout(layout: dict, path: str | Path) -> None:
    """Save layout configuration to YAML."""
    with open(path, 'w', encoding='utf-8') as fh:
        yaml.safe_dump({'layout': layout}, fh)
