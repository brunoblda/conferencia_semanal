from adobe.pdfservices.operation.io.stream_asset import StreamAsset

from project.errors.types.file_not_found import FileNotFound
from project.use_cases.interfaces.transformar_arquivos.criar_output_path import (
    CriarOutputPath as CriarOutputPathInterface,
)


class CriarOutputPathToExcelSiafi(CriarOutputPathInterface):
    def execute(self, output_file_path: str, stream_asset: StreamAsset):
        """execute the criar output path"""
        excel_path = f"{output_file_path}"
        try:
            with open(excel_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
            return excel_path
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise FileNotFound("Arquivo EXCEL criado do SIAFI não foi encontrado.")
            raise e
