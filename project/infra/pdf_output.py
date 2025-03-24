from fpdf import FPDF

from project.services.types.response_data_comparar_pis import ResponseData
from project.use_cases.interfaces.pdf_output import PdfOutput as PdfOutputInterface


class PdfOutput(PdfOutputInterface):
    def __init__(self) -> None:
        self.pdf = FPDF()

    def write_pdf(self, data: ResponseData, output_name: str) -> None:
        """write data to a file"""

        output_name_sanitized = self.sanitize_output_name(output_name)
        self.pdf.add_page()
        self.pdf.set_font(family="Courier", size=10)
        self.pdf.multi_cell(0, 10, data["response"])
        self.pdf.output(f"{output_name_sanitized}_{data['status']}.pdf", "F")
    
    def sanitize_output_name(self, output_name: str) -> str:
        return output_name.replace("/", "_")
