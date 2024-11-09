""" Util class for general functions """
import math
import os

class Utils:
    """ Util class for general functions """

    def __is_float(self, string_for_verification: str) -> str|int:
        """ Check if a string is a float """
        try:    
            float(string_for_verification)
            return string_for_verification
        except ValueError:
            return 0

    def value_hygienization(self, string_for_hygienization: str) -> float:
        """ if the value is a float, replace ',' by '.' and remove spaces, else return 0 """

        if self.__is_float(string_for_hygienization):
            if math.isnan(string_for_hygienization):
                return 0
        
        sanitized_valor = string_for_hygienization.replace('.', '').replace(',', '.').replace(' ', '')

        return float(sanitized_valor) if self.__is_float(sanitized_valor) else 0

    def get_credentials(self) -> dict:
        """ Get credentials from dict """
        client_key = 'PDF_SERVICES_CLIENT_ID'
        secret_key = 'PDF_SERVICES_CLIENT_SECRET'
        return {
            'PDF_SERVICES_CLIENT_ID': os.getenv(client_key),
            'PDF_SERVICES_CLIENT_SECRET': os.getenv(secret_key)
        }
    