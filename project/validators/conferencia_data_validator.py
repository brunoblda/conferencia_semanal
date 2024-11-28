from project.errors.types.valor_data_error import ValorDataError


def conferencia_data_validator(data_da_conferencia: str) -> None:
    ano_limite_inferior = 2000
    ano_limite_superior = 2100
    mes_limite_inferior = 1
    mes_limite_superior = 12
    dia_limite_inferior = 1
    dia_limite_superior = 31
    n_de_chars = 10

    if not data_da_conferencia:
        raise ValorDataError("Data da conferência deve estar no formato dd-mm-aaaa")
    if not isinstance(data_da_conferencia, str):
        raise ValorDataError("Data da conferência deve estar no formato dd-mm-aaaa")
    if len(data_da_conferencia) != n_de_chars:
        raise ValorDataError("Data da conferência deve estar no formato dd-mm-aaaa")
    if not data_da_conferencia[2] == "-" or not data_da_conferencia[5] == "-":
        raise ValorDataError("Data da conferência deve estar no formato dd-mm-aaaa")
    if (
        not data_da_conferencia[:2].isdigit()
        or not data_da_conferencia[3:5].isdigit()
        or not data_da_conferencia[6:].isdigit()
    ):
        raise ValorDataError("Data da conferência deve estar no formato dd-mm-aaaa")
    if not dia_limite_inferior <= int(data_da_conferencia[:2]) <= dia_limite_superior:
        raise ValorDataError("Dia da conferência deve ser entre 01 e 31")
    if not mes_limite_inferior <= int(data_da_conferencia[3:5]) <= mes_limite_superior:
        raise ValorDataError("Mês da conferência deve ser entre 01 e 12")
    if not ano_limite_inferior <= int(data_da_conferencia[6:]) <= ano_limite_superior:
        raise ValorDataError("Ano da conferência deve ser entre 2000 e 2100")
