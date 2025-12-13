import os

from project.use_cases.interfaces.criar_pastas import CriarPastas as CriarPastasInterface


class CriarPastas(CriarPastasInterface):
    """Cria pastas"""

    def execute(self) -> None:
        """Cria pastas"""
        os.makedirs("./resultados", exist_ok=True)
