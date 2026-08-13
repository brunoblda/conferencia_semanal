from project.domain.interfaces.reserva import Reserva as ReservaInterface


class ReservaSeof(ReservaInterface):

    def set(self, reserva: list) -> None:
        self.reserva: list = reserva

    def set_dict(self, dict_reserva: dict) -> None:
        self.dict_reserva: dict = dict_reserva

    def get_dict(self) -> dict:
        return self.dict_reserva

    def get(self) -> list:
        return self.reserva
    