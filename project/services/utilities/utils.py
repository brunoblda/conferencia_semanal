""" Util class for general functions """

import math
import os


class Utils:
    """Util class for general functions"""

    def __is_float(self, string_for_verification: str) -> str | int:
        """Check if a string is a float"""
        try:
            float(string_for_verification)
            return string_for_verification
        except ValueError:
            return 0

    def value_hygienization(self, string_for_hygienization: str) -> float:
        """if the value is a float, replace ',' by '.' and remove spaces, else return 0"""

        if self.__is_float(string_for_hygienization):
            if math.isnan(float(string_for_hygienization)):
                return 0

        sanitized_valor = (
            string_for_hygienization.replace(".", "").replace(",", ".").replace(" ", "")
        )

        return float(sanitized_valor) if self.__is_float(sanitized_valor) else 0

    def replace_commas_and_dots(self, texto: str):
        """ Replace commas and dots in a string """
        temp_texto = texto.replace(",", "#")
        temp_texto = temp_texto.replace(".", ",")
        texto_final = temp_texto.replace("#", ".")
        return texto_final

    def get_row_and_column(self, df):
        """ Get row and column of a DataFrame """
        row_and_column_list = []
        columns_df_name = df.columns.tolist()
        rows, cols = df.shape
        for row in range(rows):
            for col in range(cols):
                if df.iat[row, col]:
                    row_and_column_list.append((row, columns_df_name[col]))
        return row_and_column_list
        