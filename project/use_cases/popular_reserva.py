from project.domain.interfaces.reserva import Reserva as ReservaInterface
from project.use_cases.mapear.mapear_reserva import MapearReserva
from project.use_cases.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos

class PopularReserva:
    def __init__(
        self,
        mapear_reserva: MapearReserva,
        processar_dados_bruto: ProcessarDadosBrutos,
        reserva: ReservaInterface,
    ) -> None:
        self.__mapear_reserva = mapear_reserva
        self.__processar_dados_bruto = processar_dados_bruto
        self.__reserva = reserva

    def execute(
        self, input_file_path: str, output_file_name: str
    ) -> ReservaInterface:

        self.__reserva.set(
            self.__processar_dados_bruto.execute(
                input_file_path
            )
        )
        self.__reserva.set_dict(
            self.__mapear_reserva.handle(self.__reserva.get())
        )

        return self.__reserva
