from project.adapters.presenters.response_format import ResponseFormat
from project.errors.types.file_not_found import FileNotFound
from project.errors.types.sanitize_error import SanitizeError
from project.errors.types.valor_data_error import ValorDataError


def handle_error(error: Exception) -> ResponseFormat:
    """Handle error"""
    if isinstance(error, (ValorDataError, FileNotFound, SanitizeError)):
        return ResponseFormat("error", error.message, dict())
    else:
        return ResponseFormat("error", "Erro interno", {"error": error.args})
