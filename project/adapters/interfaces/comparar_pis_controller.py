from abc import ABC, abstractmethod


class CompararPisController(ABC):
    @abstractmethod
    def handle_request(
        self,
        plano_interno_principal: dict,
        plano_interno_secundario: dict,
        pdf_output_name: str,
    ) -> str:
        raise NotImplementedError("Method not implemented")
