from fpdf import FPDF, output

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Mechanical Procurement Report', 0, 1, 'C')


def generate_pdf(file_path, data_rows, total_weight):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    #table header
    pdf.cell(40, 10, "Part", 1)
    pdf.cell(30, 10, "Weight (kg)", 1)
    pdf.ln()

    for row in data_rows:
        pdf.cell(40, 10, str(row['name']), 1)
        pdf.cell(30, 10, f"{row['weight']:.2f}", 1)
        pdf.ln()


    pdf.ln(10)
    pdf.cell(0, 10, f"Total Estimated Weight: {total_weight:.2f} kg", 0, 1)
    pdf.output(file_path)
