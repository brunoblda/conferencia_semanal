from project.domain.interfaces.popular_plano_interno import PopularPlanoInterno as PopularPlanoInternoInterface
from project.domain.interfaces.plano_interno_factory import PlanoInternoFactory as PlanoInternoFactoryInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.domain.interfaces.mapear.mapear_pi import MapearPi as MapearPiInterface
from project.domain.interfaces.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos as ProcessarDadosBrutosInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class PopularPlanoInterno(PopularPlanoInternoInterface):
    def __init__ (self, mapear_pi: MapearPiInterface, processar_dados_bruto: ProcessarDadosBrutosInterface, plano_interno: PlanoInternoInterface ) -> None:
        self.__mapear_pi = mapear_pi
        self.__processar_dados_bruto = processar_dados_bruto
        self.__plano_interno = plano_interno 
    
    def execute(self, credentials: dict, input_file_path: str, output_file_name: str) -> PlanoInternoInterface:
        
        self.__plano_interno.set(self.__processar_dados_bruto.execute(credentials, input_file_path, output_file_name))
        self.__plano_interno.set_dict(self.__mapear_pi.handle(self.__plano_interno.get()))

        return self.__plano_interno