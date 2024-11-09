from project.domain.interfaces.popular_plano_interno import PopularPlanoInterno as PopularPlanoInternoInterface
from project.adapters.interfaces.popular_plano_interno_controller import PopularPlanoInternoController as PopularPlanoInternoControllerInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class PopularPlanoInternoController(PopularPlanoInternoControllerInterface):

    def __init__(self, popular_plano_interno: PopularPlanoInternoInterface) -> None:
        self.__popular_plano_interno = popular_plano_interno

    def handle_request(self, credentials: dict, input_file_path: str, output_file_name: str) -> PlanoInternoInterface:

        plano_interno_populado = self.__popular_plano_interno.execute(credentials, input_file_path, output_file_name)

        return plano_interno_populado
        