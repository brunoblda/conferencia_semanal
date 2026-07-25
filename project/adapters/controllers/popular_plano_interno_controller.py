from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.use_cases.popular_plano_interno import PopularPlanoInterno


class PopularPlanoInternoController:

    def __init__(self, popular_plano_interno: PopularPlanoInterno) -> None:
        self.__popular_plano_interno = popular_plano_interno

    def handle_request(
        self, input_file_path: str, output_file_name: str
    ) -> PlanoInternoInterface:

        plano_interno_populado = self.__popular_plano_interno.execute(
            input_file_path, output_file_name
        )

        return plano_interno_populado
