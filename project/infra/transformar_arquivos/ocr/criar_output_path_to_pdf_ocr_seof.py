from project.use_cases.interfaces.transformar_arquivos.criar_output_path import CriarOutputPath as CriarOutputPathInterface
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from project.errors.types.file_not_found import FileNotFound

class CriarOutputPathToPdfOcrSeof(CriarOutputPathInterface):
    def execute(self, output_file_path: str, stream_asset: StreamAsset):
        """ execute the criar output path """
        pdf_ocr_path = f"{output_file_path}"  
        try:
            with open(pdf_ocr_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
            return pdf_ocr_path
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise FileNotFound("Arquivo PDF OCR criado do SEOF não foi encontrado.")
            raise e 