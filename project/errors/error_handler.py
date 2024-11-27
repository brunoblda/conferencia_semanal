from project.adapters.presenters.response_format import ResponseFormat
from project.errors.types.valor_data_error import ValorDataError
from project.errors.types.file_not_found import FileNotFound
from project.errors.types.sanitize_error import SanitizeError 

def handle_error(error: Exception) -> ResponseFormat:
    """ Handle error """
    if isinstance(error, (ValorDataError, FileNotFound, SanitizeError)):
        return ResponseFormat(error.message, dict()) 
    else:
        return ResponseFormat('Erro interno', {"error": error.args} ) 
        