from project.adapters.interfaces.comparar_pis_controller import CompararPisController as CompararPisControllerInterface
from project.domain.interfaces.comparar.comparar_pis import CompararPis as CompararPisInterface
from project.domain.interfaces.mapear.mapear_pi import MapearPi as MapearPiInterface
from project.domain.interfaces.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos as ProcessarDadosBrutosInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class CompararPisController(CompararPisControllerInterface):
    """ Controller to compare PI_principal com PI_secundário """

    def __init__(self, comparar_pis: CompararPisInterface) -> None:
        """ Constructor """
        self.__comparar_pis = comparar_pis 
        
    def handle_request(self, plano_interno_principal, plano_interno_secundario) -> str:
        """ Handle the request """

        comparacao_planos_internos = self.__comparar_pis.execute(plano_interno_principal, plano_interno_secundario)

        return comparacao_planos_internos


