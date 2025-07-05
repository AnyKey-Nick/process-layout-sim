from pathlib import Path

from .gui_main import run_gui


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    run_gui(str(base / "config" / "layout.yaml"), str(base / "config" / "processes.yaml"))