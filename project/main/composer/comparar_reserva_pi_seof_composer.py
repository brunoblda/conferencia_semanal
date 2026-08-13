from project.adapters.controllers.comparar_reservas_controller import CompararReservasController
from project.adapters.controllers.popular_reserva_controller import PopularReservaController
from project.adapters.presenters.response_format import ResponseFormat
from project.domain.entities.reserva_pi import ReservaPi
from project.domain.entities.reserva_seof import ReservaSeof
from project.infra.pdf_output import PdfOutputArquivo
from project.infra.pegar_dados_processados.ler_dados_reserva_pi import LerDadosReservaPi
from project.infra.pegar_dados_processados.ler_dados_reserva_seof import LerDadosReservaSeof
from project.services.utilities.utils import Utils
from project.use_cases.comparar.comparar_reserva_pi_seof import CompararReservaPiSeof
from project.use_cases.mapear.mapear_reserva import MapearReserva
from project.use_cases.mapear.reserva.command.dicionarizar_reserva_pi import (
    DicionarizarReservaPi,
)
from project.use_cases.mapear.reserva.command.dicionarizar_reserva_seof import (
    DicionarizarReservaSeof,
)
from project.use_cases.popular_reserva import PopularReserva
from project.use_cases.processar_dados_brutos.processar_dados_brutos import (
    ProcessarDadosBrutos,
)

def comparar_reserva_pi_seof_composer(request: dict) -> ResponseFormat:
    """ Compare Reserva PI with Reserva SEOF Composer """

    input_file_path_principal = request["input_file_path_principal"]
    input_file_path_secundario = request["input_file_path_secundario"]
    data_da_conferencia = request["data_da_conferencia"]

    reserva_pi = ReservaPi()
    output_file_path_pi = f"./pdf_ocr/reserva_pi_{data_da_conferencia}.pdf"
    utils = Utils
    ler_dados_reserva_pi = LerDadosReservaPi()
    processar_dados_bruto = ProcessarDadosBrutos(
        ler_dados_reserva_pi,
    )
    dicionarizar_reserva_pi = DicionarizarReservaPi(utils)
    mapear_reserva = MapearReserva(dicionarizar_reserva_pi)
    popular_reserva = PopularReserva(
        mapear_reserva, processar_dados_bruto, reserva_pi
    )
    popular_reserva_controller = PopularReservaController(
        popular_reserva
    )

    reserva_pi_populado = popular_reserva_controller.handle_request(
        input_file_path_principal, output_file_path_pi
    )

    reserva_seof = ReservaSeof()

    output_file_path_pi_seof = f"./pdf_ocr/reserva_seof_{data_da_conferencia}.pdf"
    ler_dados_reserva_seof = LerDadosReservaSeof()
    processar_dados_bruto_seof = ProcessarDadosBrutos(
        ler_dados_reserva_seof,
    )
    dicionarizar_reserva_seof = DicionarizarReservaSeof(utils)
    mapear_reserva_seof = MapearReserva(dicionarizar_reserva_seof)
    popular_reserva_seof = PopularReserva(
        mapear_reserva_seof, processar_dados_bruto_seof, reserva_seof
    )
    popular_reserva_seof_controller = PopularReservaController(
        popular_reserva_seof
    )

    reserva_seof_populado = popular_reserva_seof_controller.handle_request(
        input_file_path_secundario, output_file_path_pi_seof
    )
    
    comparar_reserva_pi_seof = CompararReservaPiSeof(utils)
    pdf_output = PdfOutputArquivo()
    
    pdf_output_name = f"resultado_reserva_PI_SEOF_{data_da_conferencia}"
    
    comparar_reserva_pi_seof_controller = CompararReservasController(
        comparar_reserva_pi_seof, pdf_output
    )
    comparacao_reserva_pi_seof = comparar_reserva_pi_seof_controller.handle_request(
        reserva_pi_populado.get_dict(), reserva_seof_populado.get_dict(), pdf_output_name,
    )

    return comparacao_reserva_pi_seof
    