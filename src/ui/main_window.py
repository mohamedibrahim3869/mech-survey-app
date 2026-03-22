import enum
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QLabel)

from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechanical Sheet Metal Calculator")
        self.resize(1000,600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.button_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import Survey (Excel/CSV)")
        self.calc_btn = QPushButton("Calculate Weights & Sheets")
        self.export_btn = QPushButton("Export PDF Report")
        self.button_layout.addWidget(self.import_btn)
        self.button_layout.addWidget(self.calc_btn)
        self.button_layout.addWidget(self.export_btn)
        self.layout.addLayout(self.button_layout)

        #Data Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Part Name", "Length (mm)", "Width (mm)", "Thickness (mm)", "Material", "Qty"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)


        #bottom summary bar

        self.summary_label = QLabel("Total Weight: 0.00 kg | Required Sheets: -")
        self.summary_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.layout.addWidget(self.summary_label)

    def update_table(self, dataframe):
        self.table.setRowCount(0)
        self.table.setRowCount(dataframe.shape[0])
        columns = ['name', 'length', 'width', 'thickness', 'material', 'quantity']
        for i, row in dataframe.iterrows():
            for j, col_name in enumerate(columns):
                val = row.get(col_name, "")
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.summary_label.setText(f"Imported {len(dataframe)} parts. Click 'Calculate' to process.")

