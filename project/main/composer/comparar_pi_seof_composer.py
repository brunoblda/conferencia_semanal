from project.adapters.controllers.comparar_pis_controller import CompararPisController
from project.adapters.controllers.popular_plano_interno_controller import (
    PopularPlanoInternoController,
)
from project.adapters.presenters.response_format import ResponseFormat
from project.domain.entities.plano_interno import PlanoInterno
from project.domain.entities.plano_interno_seof import PlanoInternoSeof
from project.infra.pdf_output import PdfOutput
from project.infra.pegar_dados_processados.ler_dados_pi import LerDadosPi
from project.infra.pegar_dados_processados.ler_dados_seof import LerDadosSeof
from project.services.utilities.utils import Utils
from project.use_cases.comparar.comparar_pi_seof import CompararPiSeof
from project.use_cases.mapear.mapear_pi import MapearPi
from project.use_cases.mapear.pi.command.dicionarizar_indices_pi import (
    DicionarizarIndices,
)
from project.use_cases.mapear.pi.command.pegar_indices_pi import PegarIndicesPi
from project.use_cases.mapear.pi_seof.command.dicionarizar_indices_pi_seof import (
    DicionarizarIndicesPiSeof,
)
from project.use_cases.mapear.pi_seof.command.pegar_indices_pi_seof import (
    PegarIndicesPiSeof,
)
from project.use_cases.popular_plano_interno import PopularPlanoInterno
from project.use_cases.processar_dados_brutos.processar_dados_brutos import (
    ProcessarDadosBrutos,
)


def comparar_pi_seof_composer(request: dict) -> ResponseFormat:
    """Compare PI with SEOF Composer"""

    input_file_path_principal = request["input_file_path_principal"]
    input_file_path_secundario = request["input_file_path_secundario"]
    data_da_conferencia = request["data_da_conferencia"]

    plano_interno_pi = PlanoInterno()
    output_file_path_pi = f"./pdf_ocr/pi_{data_da_conferencia}.pdf"
    utils = Utils()
    ler_dados_pi = LerDadosPi()
    processar_dados_bruto = ProcessarDadosBrutos(
        ler_dados_pi,
    )
    dicionarizar_indices = DicionarizarIndices(utils)
    pegar_indices = PegarIndicesPi(utils)
    mapear_pi = MapearPi(dicionarizar_indices, pegar_indices)
    popular_plano_interno = PopularPlanoInterno(
        mapear_pi, processar_dados_bruto, plano_interno_pi
    )
    popular_plano_interno_controller = PopularPlanoInternoController(
        popular_plano_interno
    )

    plano_interno_pi_populado = popular_plano_interno_controller.handle_request(
        input_file_path_principal, output_file_path_pi
    )

    plano_interno_seof = PlanoInternoSeof()
    output_file_path_pi_seof = f"./pdf_ocr/pi_seof_{data_da_conferencia}.pdf"
    ler_dados_seof = LerDadosSeof()
    processar_dados_bruto_seof = ProcessarDadosBrutos(
        ler_dados_seof,
    )
    dicionarizar_indices_seof = DicionarizarIndicesPiSeof(utils)
    pegar_indices_seof = PegarIndicesPiSeof(utils)
    mapear_pi_seof = MapearPi(
        dicionarizar_indices_seof, pegar_indices_seof
    )
    popular_plano_interno_seof = PopularPlanoInterno(
        mapear_pi_seof, processar_dados_bruto_seof, plano_interno_seof
    )
    popular_plano_interno_controller_seof = PopularPlanoInternoController(
        popular_plano_interno_seof
    )

    plano_interno_seof_populado = popular_plano_interno_controller_seof.handle_request(
        input_file_path_secundario, output_file_path_pi_seof
    )

    comparar_pi_seof = CompararPiSeof(utils)

    pdf_output = PdfOutput()

    pdf_output_name = f"resultado_PI_SEOF_{data_da_conferencia}"

    comparar_pi_seof_controller = CompararPisController(comparar_pi_seof, pdf_output)

    comparacao_pi_seof = comparar_pi_seof_controller.handle_request(
        plano_interno_pi_populado.get_dict(),
        plano_interno_seof_populado.get_dict(),
        pdf_output_name,
    )

    return comparacao_pi_seof
