from project.domain.interfaces.reserva import Reserva as ReservaInterface
from project.use_cases.popular_reserva import PopularReserva


class PopularReservaController:

    def __init__(self, popular_reserva: PopularReserva) -> None:
        self.__popular_reserva = popular_reserva

    def handle_request(
        self, input_file_path: str, output_file_name: str
    ) -> ReservaInterface:

        reserva_populada = self.__popular_reserva.execute(
            input_file_path, output_file_name
        )

        return reserva_populada