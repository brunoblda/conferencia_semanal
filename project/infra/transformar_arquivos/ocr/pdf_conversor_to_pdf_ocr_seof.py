from project.use_cases.interfaces.transformar_arquivos.pdf_conversor import PdfConversor as PdfConversorInterface
import logging
from project.errors.types.file_not_found import FileNotFound
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job import ExportPDFJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_ocr_locale import ExportOCRLocale
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import ExportPDFTargetFormat
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_result import ExportPDFResult
from adobe.pdfservices.operation.pdfjobs.jobs.ocr_pdf_job import OCRPDFJob
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_params import OCRParams
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_locale import OCRSupportedLocale
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_type import OCRSupportedType
from adobe.pdfservices.operation.pdfjobs.result.ocr_pdf_result import OCRPDFResult

class PdfConversorToPdfOcrSeof(PdfConversorInterface):
    
    def execute(self, credentials_env: dict, input_path: str):
        """ execute the pdf conversor """
        
        # Initialize the logger
        logging.basicConfig(level=logging.INFO)

        # This sample illustrates how to perform an OCR operation on a PDF file and convert it into an searchable PDF file on
        # the basis of provided locale and SEARCHABLE_IMAGE_EXACT ocr type to keep the original image
        # (Recommended for cases requiring maximum fidelity to the original image.).
        #
        # Note that OCR operation on a PDF file results in a PDF file.
        #
        # Refer to README.md for instructions on how to run the samples.
        #

        try:
            file = open(input_path, 'rb')
            input_stream = file.read()
            file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id = credentials_env['PDF_SERVICES_CLIENT_ID'],
                client_secret = credentials_env['PDF_SERVICES_CLIENT_SECRET']
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream,
                                            mime_type=PDFServicesMediaType.PDF)

            ocr_pdf_params = OCRParams(
                ocr_locale=OCRSupportedLocale.PT_BR,
                ocr_type=OCRSupportedType.SEARCHABLE_IMAGE
            )

            # Creates a new job instance
            ocr_pdf_job = OCRPDFJob(input_asset=input_asset, ocr_pdf_params=ocr_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(ocr_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, OCRPDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)


            return stream_asset

        except Exception as e:
            if isinstance(e, (ServiceApiException, ServiceUsageException, SdkException)):
                logging.exception(f'Exception encountered while executing operation: {e}')
            if isinstance(e, FileNotFoundError):
                raise FileNotFound("Arquivo do SEOF não foi encontrado.")
            raise e
