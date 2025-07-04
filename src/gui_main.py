from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .layout_engine import load_layout
from .simulator_core import Simulator


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.figure = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.xdata = []
        self.ydata = []

    def append(self, x: float, y: float) -> None:
        self.xdata.append(x)
        self.ydata.append(y)
        if len(self.xdata) > 600:
            self.xdata = self.xdata[-600:]
            self.ydata = self.ydata[-600:]
        self.ax.clear()
        self.ax.plot(self.xdata, self.ydata)
        self.ax.set_xlim(max(0, self.xdata[-1] - 60), self.xdata[-1] + 0.001)
        self.canvas.draw()


class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, layout_path: str, process_path: str):
        super().__init__()
        self.setWindowTitle("Process Simulator")
        self.layout_cfg = load_layout(layout_path)
        self.sim = Simulator(process_path)
        self.widgets: Dict[str, QtWidgets.QWidget] = {}
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        grid = QtWidgets.QGridLayout(central)
        for element in self.layout_cfg.get('grid', {}).get('elements', []):
            pos = element['position']
            label = element.get('label', element['id'])
            if element['type'] == 'sensor':
                widget = PlotWidget()
            else:
                widget = QtWidgets.QLabel('0.0')
                widget.setAlignment(QtCore.Qt.AlignCenter)
            box = QtWidgets.QVBoxLayout()
            box_widget = QtWidgets.QWidget()
            box_widget.setLayout(box)
            box.addWidget(QtWidgets.QLabel(label))
            box.addWidget(widget)
            grid.addWidget(box_widget, *pos)
            self.widgets[element['id']] = widget
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.start_time = QtCore.QTime.currentTime()
        self.timer.start(100)

    def update_simulation(self) -> None:
        t = self.start_time.msecsTo(QtCore.QTime.currentTime()) / 1000.0
        values = self.sim.step(0.1)
        for key, val in values.items():
            w = self.widgets.get(key)
            if isinstance(w, PlotWidget):
                w.append(t, val)
            elif isinstance(w, QtWidgets.QLabel):
                w.setText(f"{val:.2f}")


def run_gui(layout_file: str, process_file: str) -> None:
    app = QtWidgets.QApplication(sys.argv)
    win = Dashboard(layout_file, process_file)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    run_gui(base / "config" / "layout.yaml", base / "config" / "processes.yaml")
