from fpdf import FPDF
from datetime import datetime

class EngineeringReport(FPDF):
    def header(self):
        # Logo or Title
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Material Procurement & Weight Survey', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_procurement_pdf(output_path, survey_results, grand_total_weight):
    pdf = EngineeringReport()
    pdf.add_page()
    
    # Table Header Styling
    pdf.set_fill_color(44, 62, 80) # Dark Blue
    pdf.set_text_color(255, 255, 255) # White
    pdf.set_font('Arial', 'B', 11)
    
    # Define Column Widths
    cols = [50, 40, 35, 35, 30]
    headers = ['Material', 'Thickness', 'Net Wt (kg)', 'Buy Wt (kg)', 'Sheets']
    
    for i, header in enumerate(headers):
        pdf.cell(cols[i], 10, header, 1, 0, 'C', True)
    pdf.ln()

    # Table Body
    pdf.set_text_color(0, 0, 0) # Back to Black
    pdf.set_font('Arial', '', 10)
    
    for row in survey_results:
        pdf.cell(cols[0], 10, str(row['material']), 1)
        pdf.cell(cols[1], 10, f"{row['thickness']} mm", 1, 0, 'C')
        pdf.cell(cols[2], 10, f"{row['net_weight']:.2f}", 1, 0, 'R')
        pdf.cell(cols[3], 10, f"{row['buy_weight']:.2f}", 1, 0, 'R')
        pdf.cell(cols[4], 10, str(row['sheets']), 1, 0, 'C')
        pdf.ln()

    # Grand Total
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Total Project Weight: {grand_total_weight:.2f} kg", 0, 1, 'R')
    
    pdf.output(output_path)
