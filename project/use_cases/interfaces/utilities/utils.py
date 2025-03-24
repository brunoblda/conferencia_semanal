from abc import ABC, abstractmethod


class Utils(ABC):
    @abstractmethod
    def __is_float(self, string_for_verification: str) -> bool:
        """check if value is float"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def value_hygienization(self, string_for_hygienization: str) -> float:
        """if the value is a float, replace ',' by '.' and remove spaces,
        else return 0"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def replace_commas_and_dots(self, texto: str):
        """Change commas and dots"""
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def get_row_and_column(self, df):
        """Get row and column of a DataFrame"""
        raise NotImplementedError("Method not implemented")
