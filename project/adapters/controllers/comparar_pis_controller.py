from project.adapters.interfaces.comparar_pis_controller import CompararPisController as CompararPisControllerInterface
from project.domain.interfaces.comparar.comparar_pis import CompararPis as CompararPisInterface
from project.domain.interfaces.mapear.mapear_pi import MapearPi as MapearPiInterface
from project.domain.interfaces.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos as ProcessarDadosBrutosInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.use_cases.interfaces.pdf_output import PdfOutput as PdfOutputInterface
from project.adapters.presenters.response_format import ResponseFormat

class CompararPisController(CompararPisControllerInterface):
    """ Controller to compare PI_principal com PI_secundário """

    def __init__(self, comparar_pis: CompararPisInterface, pdf_output: PdfOutputInterface) -> None:
        """ Constructor """
        self.__comparar_pis = comparar_pis 
        self.__pdf_output = pdf_output
        
    def handle_request(self, plano_interno_principal: dict, plano_interno_secundario: dict, pdf_output_name: str) -> str:
        """ Handle the request """

        comparacao_planos_internos = self.__comparar_pis.execute(plano_interno_principal, plano_interno_secundario)
        self.__pdf_output.write_pdf(comparacao_planos_internos, pdf_output_name)

        return ResponseFormat(message='Comparação realizada com sucesso!',body={'data':comparacao_planos_internos})


