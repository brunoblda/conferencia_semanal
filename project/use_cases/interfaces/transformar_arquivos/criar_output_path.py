from abc import ABC, abstractmethod

from adobe.pdfservices.operation.io.stream_asset import StreamAsset


class CriarOutputPath(ABC):
    @abstractmethod
    def execute(self, output_file_path: str, stream_asset: StreamAsset):
        """execute the criar output path"""
        raise NotImplementedError("Method not implemented")
