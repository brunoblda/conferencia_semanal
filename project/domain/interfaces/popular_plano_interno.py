from abc import ABC, abstractmethod


class PopularPlanoInterno(ABC):
    @abstractmethod
    def execute(
        self, credentials: dict, input_file_path: str, output_file_name: str
    ) -> str:
        """handle the popular plano interno"""
        raise NotImplementedError("Method not implemented")
