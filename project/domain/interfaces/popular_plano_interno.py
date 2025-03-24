from abc import ABC, abstractmethod


class PopularPlanoInterno(ABC):
    @abstractmethod
    def execute(
        self, input_file_path: str 
    ) -> str:
        """handle the popular plano interno"""
        raise NotImplementedError("Method not implemented")
