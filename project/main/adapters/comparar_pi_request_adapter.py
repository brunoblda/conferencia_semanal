
def comparar_pi_request_adapter(input_file_path_principal: str, input_file_path_secundario: str, data_da_conferencia: str) -> dict:
    """ Request Adapter """

    if input_file_path_principal[0] == "\'" or input_file_path_principal[0] == "\"":
        input_file_path_principal = input_file_path_principal[1:] 
    if input_file_path_principal[-1] == "\'" or input_file_path_principal[-1] == "\"":
        input_file_path_principal = input_file_path_principal[:-1]

    if input_file_path_secundario[0] == "\'" or input_file_path_secundario[0] == "\"":
        input_file_path_secundario = input_file_path_secundario[1:]
    if input_file_path_secundario[-1] == "\'" or input_file_path_secundario[-1] == "\"":
        input_file_path_secundario = input_file_path_secundario[:-1]

    response_dict = {
        "input_file_path_principal": input_file_path_principal,
        "input_file_path_secundario": input_file_path_secundario,
        "data_da_conferencia": data_da_conferencia
    }

    return response_dict