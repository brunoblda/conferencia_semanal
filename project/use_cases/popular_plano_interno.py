from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.use_cases.mapear.mapear_pi import MapearPi
from project.use_cases.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos


class PopularPlanoInterno:
    def __init__(
        self,
        mapear_pi: MapearPi,
        processar_dados_bruto: ProcessarDadosBrutos,
        plano_interno: PlanoInternoInterface,
    ) -> None:
        self.__mapear_pi = mapear_pi
        self.__processar_dados_bruto = processar_dados_bruto
        self.__plano_interno = plano_interno

    def execute(
        self, input_file_path: str, output_file_name: str
    ) -> PlanoInternoInterface:

        self.__plano_interno.set(
            self.__processar_dados_bruto.execute(
                input_file_path
            )
        )
        self.__plano_interno.set_dict(
            self.__mapear_pi.handle(self.__plano_interno.get())
        )

        return self.__plano_interno
