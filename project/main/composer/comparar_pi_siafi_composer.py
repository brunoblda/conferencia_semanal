from project.domain.entities.plano_interno import PlanoInterno
from project.domain.entities.plano_interno_siafi import PlanoInternoSiafi
from project.use_cases.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos
from project.infra.transformar_arquivos.ocr.pdf_conversor_to_pdf_ocr import PdfConversorToPdfOcr
from project.infra.transformar_arquivos.ocr.criar_output_path_to_pdf_ocr import CriarOutputPathToPdfOcr
from project.infra.transformar_arquivos.excel.pdf_conversor_to_excel import PdfConversorToExcel
from project.infra.transformar_arquivos.excel.criar_output_path_to_excel import CriarOutputPathToExcel
from project.infra.pegar_dados_processados.ler_dados_pi import LerDadosPi
from project.infra.pegar_dados_processados.ler_dados_siafi import LerDadosSiafi
from project.infra.transformar_arquivos.verificar_existencia_de_arquivo import VerificarExistenciaDeArquivo
from project.use_cases.mapear.mapear_pi import MapearPi
from project.use_cases.mapear.pi.command.sanitizar_pi import SanitizarPi
from project.use_cases.mapear.pi.command.dicionarizar_indices_pi import DicionarizarIndices
from project.use_cases.mapear.pi.command.pegar_indices_pi import PegarIndicesPi
from project.services.utilities.utils import Utils
from project.use_cases.mapear.pi_siafi.command.dicionarizar_indices_pi_siafi import DicionarizarIndicesPiSiafi
from project.use_cases.mapear.pi_siafi.command.pegar_indices_pi_siafi import PegarIndicesPiSiafi
from project.use_cases.mapear.pi_siafi.command.sanitizar_pi_siafi import SanitizarPiSiafi
from project.use_cases.popular_plano_interno import PopularPlanoInterno
from project.adapters.controllers.popular_plano_interno_controller import PopularPlanoInternoController
from project.use_cases.comparar.comparar_pi_siafi import CompararPiSiafi
from project.adapters.controllers.comparar_pis_controller import CompararPisController

def comparar_pi_siafi_composer(input_file_path_principal: str, input_file_path_secundario: str, data_da_conferencia: str) -> str:
    """ Compare PI with SIAFI Composer """
    plano_interno_pi = PlanoInterno()
    output_file_path_pi = f"../pdf_ocr/pi_{data_da_conferencia}.pdf"
    utils = Utils()
    credentials = utils.get_credentials()
    criar_output_path_to_pdf_ocr = CriarOutputPathToPdfOcr()
    ler_dados_pi = LerDadosPi()
    pdf_conversor_to_pdf_ocr = PdfConversorToPdfOcr()
    verificar_existencia_de_arquivo = VerificarExistenciaDeArquivo()
    processar_dados_bruto = ProcessarDadosBrutos(ler_dados_pi, pdf_conversor_to_pdf_ocr, criar_output_path_to_pdf_ocr, verificar_existencia_de_arquivo)
    sanitizar_pi = SanitizarPi()
    dicionarizar_indices = DicionarizarIndices(utils)
    pegar_indices = PegarIndicesPi()
    mapear_pi = MapearPi(dicionarizar_indices, sanitizar_pi, pegar_indices)
    popular_plano_interno = PopularPlanoInterno(mapear_pi, processar_dados_bruto, plano_interno_pi)
    popular_plano_interno_controller = PopularPlanoInternoController(popular_plano_interno)

    plano_interno_pi_populado = popular_plano_interno_controller.handle_request(credentials, input_file_path_principal, output_file_path_pi)

    pdf_conversor_to_excel = PdfConversorToExcel()
    criar_output_path_to_excel = CriarOutputPathToExcel()
    plano_interno_siafi = PlanoInternoSiafi()
    output_file_path_pi_siafi = f"../excel/pi_siafi_{data_da_conferencia}.xlsx"
    ler_dados_siafi = LerDadosSiafi()
    processar_dados_bruto_siafi = ProcessarDadosBrutos(ler_dados_siafi, pdf_conversor_to_excel, criar_output_path_to_excel, verificar_existencia_de_arquivo)
    sanitiza_pi_siafi = SanitizarPiSiafi()
    dicionarizar_indices_siafi = DicionarizarIndicesPiSiafi(utils)
    pegar_indices_siafi = PegarIndicesPiSiafi()
    mapear_pi_siafi = MapearPi(dicionarizar_indices_siafi, sanitiza_pi_siafi, pegar_indices_siafi)
    popular_plano_interno_siafi = PopularPlanoInterno(mapear_pi_siafi, processar_dados_bruto_siafi, plano_interno_siafi)
    popular_plano_interno_controller_siafi = PopularPlanoInternoController(popular_plano_interno_siafi)

    plano_interno_siafi_populado = popular_plano_interno_controller_siafi.handle_request(credentials, input_file_path_secundario, output_file_path_pi_siafi)

    comparar_pi_siafi = CompararPiSiafi()
    comparar_pi_siafi_controller = CompararPisController(comparar_pi_siafi)
    
    comparacao_pi_siafi = comparar_pi_siafi_controller.handle_request(plano_interno_pi_populado.get_dict(), plano_interno_siafi_populado.get_dict())

    return comparacao_pi_siafi