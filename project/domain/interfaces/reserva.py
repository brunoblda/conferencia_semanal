from abc import ABC, abstractmethod


class Reserva(ABC):
    @abstractmethod
    def set(self, reserva):
        """set the reserva"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def set_dict(self, dict_reserva):
        """set the dict reserva"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_dict(self):
        """get the dict reserva"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get(self):
        """get the reserva"""
        raise NotImplementedError("Method not implemented")