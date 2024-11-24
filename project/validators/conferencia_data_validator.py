from project.errors.types.valor_data_error import ValorDataError


def conferencia_data_validator(data_da_conferencia: str) -> None:
    if not data_da_conferencia:
        raise ValorDataError('Data da conferência deve estar no formato dd-mm-aaaa')
    if not isinstance(data_da_conferencia, str):
        raise ValorDataError('Data da conferência deve estar no formato dd-mm-aaaa')
    if len(data_da_conferencia) != 10:
        raise ValorDataError('Data da conferência deve estar no formato dd-mm-aaaa')
    if not data_da_conferencia[2] == '-' or not data_da_conferencia[5] == '-':
        raise ValorDataError('Data da conferência deve estar no formato dd-mm-aaaa')
    if not data_da_conferencia[:2].isdigit() or not data_da_conferencia[3:5].isdigit() or not data_da_conferencia[6:].isdigit():
        raise ValorDataError('Data da conferência deve estar no formato dd-mm-aaaa')
    if not 1 <= int(data_da_conferencia[:2]) <= 31:
        raise ValorDataError('Dia da conferência deve ser entre 01 e 31')
    if not 1 <= int(data_da_conferencia[3:5]) <= 12:
        raise ValorDataError('Mês da conferência deve ser entre 01 e 12')
    if not 2000 <= int(data_da_conferencia[6:]) <= 2100:
        raise ValorDataError('Ano da conferência deve ser entre 2000 e 2100')