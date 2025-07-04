from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

from functools import partial

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

        main_layout = QtWidgets.QHBoxLayout(central)
        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        main_layout.addWidget(grid_widget)
        control_widget = self._build_control_panel()
        main_layout.addWidget(control_widget)

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

    def _build_control_panel(self) -> QtWidgets.QWidget:
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        self.start_btn = QtWidgets.QPushButton("Pause")
        self.start_btn.clicked.connect(self._toggle_timer)
        layout.addWidget(self.start_btn)
        for name, ctrl in self.sim.controllers.items():
            box = QtWidgets.QGroupBox(name)
            form = QtWidgets.QFormLayout(box)
            type_combo = QtWidgets.QComboBox()
            type_combo.addItems(["P", "PI", "PID"])
            form.addRow("Type", type_combo)
            sp_spin = QtWidgets.QDoubleSpinBox()
            sp_spin.setRange(-1e6, 1e6)
            sp_spin.setValue(ctrl.cfg.setpoint)
            form.addRow("Setpoint", sp_spin)
            kp_spin = QtWidgets.QDoubleSpinBox()
            kp_spin.setRange(-1e6, 1e6)
            kp_spin.setValue(ctrl.cfg.Kp)
            form.addRow("Kp", kp_spin)
            ki_spin = QtWidgets.QDoubleSpinBox()
            ki_spin.setRange(-1e6, 1e6)
            ki_spin.setValue(ctrl.cfg.Ki)
            form.addRow("Ki", ki_spin)
            kd_spin = QtWidgets.QDoubleSpinBox()
            kd_spin.setRange(-1e6, 1e6)
            kd_spin.setValue(ctrl.cfg.Kd)
            form.addRow("Kd", kd_spin)

            sp_spin.valueChanged.connect(partial(self._update_setpoint, ctrl))
            kp_spin.valueChanged.connect(partial(self._update_kp, ctrl))
            ki_spin.valueChanged.connect(partial(self._update_ki, ctrl))
            kd_spin.valueChanged.connect(partial(self._update_kd, ctrl))
            type_combo.currentTextChanged.connect(partial(self._update_type, ctrl, ki_spin, kd_spin))

            layout.addWidget(box)
        layout.addStretch()
        return panel

    def _toggle_timer(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.start_time = QtCore.QTime.currentTime()
            self.timer.start(100)
            self.start_btn.setText("Pause")

    def _update_setpoint(self, ctrl, val):
        ctrl.cfg.setpoint = val

    def _update_kp(self, ctrl, val):
        ctrl.cfg.Kp = val

    def _update_ki(self, ctrl, val):
        ctrl.cfg.Ki = val

    def _update_kd(self, ctrl, val):
        ctrl.cfg.Kd = val

    def _update_type(self, ctrl, ki_spin, kd_spin, text):
        if text == "P":
            ctrl.cfg.Ki = 0.0
            ctrl.cfg.Kd = 0.0
            ki_spin.setValue(0.0)
            kd_spin.setValue(0.0)
        elif text == "PI":
            ctrl.cfg.Kd = 0.0
            kd_spin.setValue(0.0)
        # PID keeps existing Ki and Kd
        return None


def run_gui(layout_file: str, process_file: str) -> None:
    app = QtWidgets.QApplication(sys.argv)
    win = Dashboard(layout_file, process_file)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    run_gui(base / "config" / "layout.yaml", base / "config" / "processes.yaml")
