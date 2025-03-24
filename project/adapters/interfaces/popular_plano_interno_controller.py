from abc import ABC, abstractmethod


class PopularPlanoInternoController(ABC):
    @abstractmethod
    def handle_request(
        self, input_file_path: str, output_file_name: str
    ) -> str:
        raise NotImplementedError("Method not implemented")
