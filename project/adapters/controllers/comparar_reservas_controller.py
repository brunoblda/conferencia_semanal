from project.adapters.presenters.response_format import ResponseFormat
from project.domain.interfaces.comparar.comparar_reservas import (
    CompararReservas as CompararReservasInterface,
)
from project.services.types.response_data_comparar_reservas import ResponseData
from project.use_cases.interfaces.pdf_output import PdfOutput as PdfOutputInterface

class CompararReservasController:
    """Controller to compare reserva PI with reserva SIAFI"""

    def __init__(
        self, comparar_reservas: CompararReservasInterface, pdf_output: PdfOutputInterface
    ) -> None:
        """Constructor"""
        self.__comparar_reservas = comparar_reservas
        self.__pdf_output = pdf_output

    def handle_request(
        self,
        reserva_principal: dict,
        reserva_secundaria: dict,
        pdf_output_name: str,
    ) -> str:
        """Handle the request"""

        comparacao_reservas: ResponseData = self.__comparar_reservas.execute(
            reserva_principal, reserva_secundaria
        )
        self.__pdf_output.write_pdf(comparacao_reservas, pdf_output_name)

        return ResponseFormat(
            status=f"success - {comparacao_reservas['status']}",
            message=f"Comparação realizada com sucesso! {comparacao_reservas['status']}",
            body=comparacao_reservas,
        )
        