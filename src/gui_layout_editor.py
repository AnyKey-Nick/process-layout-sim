from __future__ import annotations

import yaml
from PyQt5 import QtCore, QtWidgets


class LayoutEditor(QtWidgets.QDialog):
    def __init__(self, layout_path: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Layout Editor")
        self.layout_path = layout_path
        with open(layout_path, "r", encoding="utf-8") as fh:
            self.cfg = yaml.safe_load(fh) or {}
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["id", "x", "y", "type", "label"])
        btn_add = QtWidgets.QPushButton("Add")
        btn_remove = QtWidgets.QPushButton("Remove")
        btn_save = QtWidgets.QPushButton("Save")
        btn_add.clicked.connect(self.add_row)
        btn_remove.clicked.connect(self.remove_row)
        btn_save.clicked.connect(self.save)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_remove)
        hbox.addWidget(btn_save)
        layout.addLayout(hbox)
        self.load_rows()

    def load_rows(self) -> None:
        elements = self.cfg.get("layout", {}).get("grid", {}).get("elements", [])
        for el in elements:
            self.add_row(el)

    def add_row(self, el: dict | None = None) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        if el is None:
            el = {"id": "", "position": [0, 0], "type": "sensor", "label": ""}
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(el.get("id", "")))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(el["position"][0])))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(el["position"][1])))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(el.get("type", "sensor")))
        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(el.get("label", "")))

    def remove_row(self) -> None:
        r = self.table.currentRow()
        if r >= 0:
            self.table.removeRow(r)

    def save(self) -> None:
        elements = []
        for r in range(self.table.rowCount()):
            el = {
                "id": self.table.item(r, 0).text(),
                "position": [int(self.table.item(r, 1).text()), int(self.table.item(r, 2).text())],
                "type": self.table.item(r, 3).text(),
                "label": self.table.item(r, 4).text(),
            }
            elements.append(el)
        self.cfg.setdefault("layout", {}).setdefault("grid", {})["elements"] = elements
        with open(self.layout_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(self.cfg, fh)
        self.accept()
