from abc import ABC, abstractmethod

class DicionarizarReserva(ABC):
    @abstractmethod
    def execute(self, pi_reserva_list: list) -> dict:
        """execute the dicionarizar reserva """
        raise NotImplementedError("Method not implemented")