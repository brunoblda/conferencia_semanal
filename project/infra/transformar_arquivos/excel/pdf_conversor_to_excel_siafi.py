import logging

from adobe.pdfservices.operation.auth.service_principal_credentials import (
    ServicePrincipalCredentials,
)
from adobe.pdfservices.operation.exception.exceptions import (
    SdkException,
    ServiceApiException,
    ServiceUsageException,
)
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job import ExportPDFJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_ocr_locale import (
    ExportOCRLocale,
)
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import (
    ExportPDFParams,
)
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import (
    ExportPDFTargetFormat,
)
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_result import ExportPDFResult

from project.errors.types.file_not_found import FileNotFound
from project.use_cases.interfaces.transformar_arquivos.pdf_conversor import (
    PdfConversor as PdfConversorInterface,
)


class PdfConversorToExcelSiafi(PdfConversorInterface):

    def execute(self, credentials_env: dict, input_path: str):

        # Initialize the logger
        logging.basicConfig(level=logging.INFO)

        #
        # This sample illustrates how to export a PDF file to a Excel (XLSX) file. The OCR processing is also performed on
        # the input PDF file to extract text from images in the document.
        #
        # Refer to README.md for instructions on how to run the samples.
        #

        try:
            file = open(input_path, "rb")
            input_stream = file.read()
            file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=credentials_env["PDF_SERVICES_CLIENT_ID"],
                client_secret=credentials_env["PDF_SERVICES_CLIENT_SECRET"],
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(
                input_stream=input_stream, mime_type=PDFServicesMediaType.PDF
            )

            # Create parameters for the job
            export_pdf_params = ExportPDFParams(
                target_format=ExportPDFTargetFormat.XLSX, ocr_lang=ExportOCRLocale.PT_BR
            )

            # Creates a new job instance
            export_pdf_job = ExportPDFJob(
                input_asset=input_asset, export_pdf_params=export_pdf_params
            )

            # Submit the job and gets the job result
            location = pdf_services.submit(export_pdf_job)
            pdf_services_response = pdf_services.get_job_result(
                location, ExportPDFResult
            )

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it

            return stream_asset

        except Exception as e:
            if isinstance(e, (ServiceApiException, ServiceUsageException, SdkException)):
                logging.exception(
                    f"Exception encountered while executing operation: {e}"
                )
            if isinstance(e, FileNotFoundError):
                raise FileNotFound("Arquivo do SIAFI não foi encontrado.")
            raise e
