from project.domain.entities.plano_interno import PlanoInterno
from project.domain.entities.plano_interno_seof import PlanoInternoSeof
from project.use_cases.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos
from project.infra.transformar_arquivos.ocr.pdf_conversor_to_pdf_ocr_seof import PdfConversorToPdfOcrSeof
from project.infra.transformar_arquivos.ocr.criar_output_path_to_pdf_ocr_seof import CriarOutputPathToPdfOcrSeof
from project.infra.transformar_arquivos.ocr.pdf_conversor_to_pdf_ocr_pi import PdfConversorToPdfOcrPi
from project.infra.transformar_arquivos.ocr.criar_output_path_to_pdf_ocr_pi import CriarOutputPathToPdfOcrPi
from project.infra.pegar_dados_processados.ler_dados_pi import LerDadosPi
from project.infra.pegar_dados_processados.ler_dados_seof import LerDadosSeof
from project.infra.transformar_arquivos.verificar_existencia_de_arquivo import VerificarExistenciaDeArquivo
from project.use_cases.mapear.mapear_pi import MapearPi
from project.use_cases.mapear.pi.command.sanitizar_pi import SanitizarPi
from project.use_cases.mapear.pi.command.dicionarizar_indices_pi import DicionarizarIndices
from project.use_cases.mapear.pi.command.pegar_indices_pi import PegarIndicesPi
from project.services.utilities.utils import Utils
from project.use_cases.mapear.pi_seof.command.dicionarizar_indices_pi_seof import DicionarizarIndicesPiSeof
from project.use_cases.mapear.pi_seof.command.pegar_indices_pi_seof import PegarIndicesPiSeof
from project.use_cases.mapear.pi_seof.command.sanitizar_pi_seof import SanitizarPiSeof
from project.use_cases.popular_plano_interno import PopularPlanoInterno
from project.adapters.controllers.popular_plano_interno_controller import PopularPlanoInternoController
from project.use_cases.comparar.comparar_pi_seof import CompararPiSeof
from project.infra.pdf_output import PdfOutput
from project.adapters.controllers.comparar_pis_controller import CompararPisController 
from project.adapters.presenters.response_format import ResponseFormat


def comparar_pi_seof_composer(request: dict) ->  ResponseFormat: 
    """ Compare PI with SEOF Composer """
    
    input_file_path_principal = request['input_file_path_principal']
    input_file_path_secundario = request['input_file_path_secundario']
    data_da_conferencia = request['data_da_conferencia']

    plano_interno_pi = PlanoInterno()
    output_file_path_pi = f"./pdf_ocr/pi_{data_da_conferencia}.pdf"
    utils = Utils()
    credentials = utils.get_credentials()
    criar_output_path_to_pdf_ocr_pi = CriarOutputPathToPdfOcrPi()
    ler_dados_pi = LerDadosPi()
    pdf_conversor_to_pdf_ocr_pi = PdfConversorToPdfOcrPi()
    verificar_existencia_de_arquivo = VerificarExistenciaDeArquivo()
    processar_dados_bruto = ProcessarDadosBrutos(ler_dados_pi, pdf_conversor_to_pdf_ocr_pi, criar_output_path_to_pdf_ocr_pi, verificar_existencia_de_arquivo)
    sanitizar_pi = SanitizarPi()
    dicionarizar_indices = DicionarizarIndices(utils)
    pegar_indices = PegarIndicesPi()
    mapear_pi = MapearPi(dicionarizar_indices, sanitizar_pi, pegar_indices)
    popular_plano_interno = PopularPlanoInterno(mapear_pi, processar_dados_bruto, plano_interno_pi)
    popular_plano_interno_controller = PopularPlanoInternoController(popular_plano_interno)

    plano_interno_pi_populado = popular_plano_interno_controller.handle_request(credentials, input_file_path_principal, output_file_path_pi)

    plano_interno_seof = PlanoInternoSeof()
    output_file_path_pi_seof = f"./pdf_ocr/pi_seof_{data_da_conferencia}.pdf"
    criar_output_path_to_pdf_ocr_seof = CriarOutputPathToPdfOcrSeof()
    ler_dados_seof = LerDadosSeof()
    pdf_conversor_to_pdf_ocr_seof = PdfConversorToPdfOcrSeof()
    processar_dados_bruto_seof = ProcessarDadosBrutos(ler_dados_seof, pdf_conversor_to_pdf_ocr_seof, criar_output_path_to_pdf_ocr_seof, verificar_existencia_de_arquivo)
    sanitiza_pi_seof = SanitizarPiSeof()
    dicionarizar_indices_seof = DicionarizarIndicesPiSeof(utils)
    pegar_indices_seof = PegarIndicesPiSeof()
    mapear_pi_seof = MapearPi(dicionarizar_indices_seof, sanitiza_pi_seof, pegar_indices_seof)
    popular_plano_interno_seof = PopularPlanoInterno(mapear_pi_seof, processar_dados_bruto_seof, plano_interno_seof)
    popular_plano_interno_controller_seof = PopularPlanoInternoController(popular_plano_interno_seof)

    plano_interno_seof_populado = popular_plano_interno_controller_seof.handle_request(credentials, input_file_path_secundario, output_file_path_pi_seof)

    comparar_pi_seof = CompararPiSeof()

    pdf_output = PdfOutput()

    pdf_output_name = f"resultado_PI_SEOF_{data_da_conferencia}"

    comparar_pi_seof_controller = CompararPisController(comparar_pi_seof, pdf_output)

    comparacao_pi_seof = comparar_pi_seof_controller.handle_request(plano_interno_pi_populado.get_dict(), plano_interno_seof_populado.get_dict(), pdf_output_name)

    return comparacao_pi_seof
