import sys

from PyQt6.QtWidgets import QApplication, QFileDialog
from ui.main_window import MainWindow

from utils.importer import smart_load_survey as load_survey_file

from utils.exporter import generate_procurement_pdf
from engine.calculator import MetalCalculator


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

        self.calc_engine = MetalCalculator('src/engine/materials.json')

        self.window.import_btn.clicked.connect(self.handle_import)
        self.window.calc_btn.clicked.connect(self.perform_survey_analysis)
        self.window.export_btn.clicked.connect(self.handle_export)

        self.window.show()
        sys.exit(self.app.exec())

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(
                None, "Open Survey", "", "Excel Files (*.xlsx *.xls);;CSV (*.csv)"
                )

        if file_path:
            df = load_survey_file(file_path)
            if df is not None:
                self.window.update_table(df)
    def handle_calculate(self):
        total_w = 0
        for row in range(self.window.table.rowCount()):
            l = float(self.window.table.item(row,1).text())
            w = float(self.window.table.item(row,2).text())
            t = float(self.window.table.item(row,3).text())
            mat = self.window.table.item(row,4).text()
            qty = int(self.window.table.item(row, 5).text())
            weight = self.calc_engine.calculate_part_mass(l, w, t, mat) * qty
            total_w += weight
        self.window.summary_label.setText(f"Total Weight: {total_w:.2f} kg")
        self.current_total_weight = total_w
    def handle_export(self):
    if not hasattr(self, 'last_results') or not self.last_results:
        # Show a warning if they haven't calculated anything yet
        return

    save_path, _ = QFileDialog.getSaveFileName(
        None, "Save Procurement Report", "data/output/report.pdf", "PDF Files (*.pdf)"
    )
    
    if save_path:
        try:
            generate_procurement_pdf(
                save_path, 
                self.last_results, 
                self.grand_total
            )
            print(f"Report saved to {save_path}")
        except Exception as e:
            print(f"Export failed: {e}")
    def perform_survey_analysis(self):
        # 1. Collect data from table into a list of dicts
        parts = []
        for row in range(self.window.table.rowCount()):
            parts.append({
                'length': float(self.window.table.item(row, 1).text()),
                'width': float(self.window.table.item(row, 2).text()),
                'thickness': float(self.window.table.item(row, 3).text()),
                'material': self.window.table.item(row, 4).text(),
                'qty': int(self.window.table.item(row, 5).text())
            })

        # 2. Group by Material + Thickness
        results = {}
        for p in parts:
            key = (p['material'], p['thickness'])
            mass = self.calc_engine.calculate_part_mass(p['length'], p['width'], p['thickness'], p['material']) * p['qty']
            area = (p['length'] * p['width'] * p['qty'])
            
            if key not in results:
                results[key] = {'total_weight': 0, 'total_area': 0}
            
            results[key]['total_weight'] += mass
            results[key]['total_area'] += area

        # 3. Final calculation: How many sheets for each group?
        final_text = "SURVEY RESULTS:\n"
        for (mat, thk), stats in results.items():
            sheets, sheet_type = self.calc_engine.estimate_sheets_needed(stats['total_area'], mat)
            final_text += f"- {mat} ({thk}mm): {stats['total_weight']:.1f}kg -> Buy {sheets} sheets ({sheet_type})\n"
        
        self.window.summary_label.setText(final_text)

if __name__ == "__main__":
    AppController()
