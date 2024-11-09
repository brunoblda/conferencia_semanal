from project.use_cases.interfaces.pdf_output import PdfOutput as PdfOutputInterface
from fpdf import FPDF

class PdfOutput(PdfOutputInterface):
    def __init__(self) -> None:
        self.pdf = FPDF()
    
    def write_pdf(self, data: str, output_name: str) -> None:
        """ write data to a file """
        self.pdf.add_page()
        self.pdf.set_font(family='Courier', size=10)
        self.pdf.multi_cell(0, 10, data)
        self.pdf.output(f'{output_name}.pdf', 'F')
