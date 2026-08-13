""" Util class for general functions """

import math


class Utils:
    """Util class for general functions"""

    @staticmethod
    def __is_float(string_for_verification: str) -> bool:
        """Check if a string can be converted to float."""
        try:
            float(string_for_verification)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_numero(value: object) -> bool:
        """Check if a value represents a valid number in pt-BR/EN formats."""
        if value is None:
            return False

        string_value = str(value).strip()
        if not string_value or string_value.lower() == "nan":
            return False

        if string_value == '-':
            return True

        sanitized_value = (
            string_value.replace(".", "").replace(",", ".").replace(" ", "")
        )
        if not Utils.__is_float(sanitized_value):
            return False

        return not math.isnan(float(sanitized_value))

    @staticmethod
    def value_hygienization(string_for_hygienization: str) -> float:
        """if the value is a float, replace ',' by '.' and remove spaces, else return 0"""

        if Utils.__is_float(string_for_hygienization):
            if math.isnan(float(string_for_hygienization)):
                return 0

        sanitized_valor = (
            string_for_hygienization.replace(".", "").replace(",", ".").replace(" ", "")
        )

        return float(sanitized_valor) if Utils.__is_float(sanitized_valor) else 0

    @staticmethod
    def replace_commas_and_dots(texto: str) -> str:
        """ Replace commas and dots in a string """
        temp_texto = texto.replace(",", "#")
        temp_texto = temp_texto.replace(".", ",")
        texto_final = temp_texto.replace("#", ".")
        return texto_final

    @staticmethod
    def get_row_and_column(df):
        """ Get row and column of a DataFrame """
        row_and_column_list = []
        columns_df_name = df.columns.tolist()
        rows, cols = df.shape
        for row in range(rows):
            for col in range(cols):
                if df.iat[row, col]:
                    row_and_column_list.append((row, columns_df_name[col]))
        return row_and_column_list
        