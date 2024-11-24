from project.domain.interfaces.processar_dados_brutos.processar_dados_brutos import ProcessarDadosBrutos as ProcessarDadosBrutosInterface
from project.use_cases.interfaces.pegar_dados_processados.ler_dados import LerDados as LerDadosInterface
from project.use_cases.interfaces.transformar_arquivos.pdf_conversor import PdfConversor as PdfConversorInterface
from project.use_cases.interfaces.transformar_arquivos.criar_output_path import CriarOutputPath as CriarOutputPathInterface
from project.use_cases.interfaces.transformar_arquivos.verificar_existencia_de_arquivo import VerificarExistenciaDeArquivo as VerificarExistenciaDeArquivoInterface
import pandas as pd

class ProcessarDadosBrutos(ProcessarDadosBrutosInterface):
    def __init__(self, ler_dados: LerDadosInterface, pdf_conversor: PdfConversorInterface, criar_output_path: CriarOutputPathInterface , verificar_existencia_de_arquivo: VerificarExistenciaDeArquivoInterface) -> None:
        """ Constructor  """

        self.__ler_dados = ler_dados
        self.__pdf_conversor = pdf_conversor
        self.__criar_output_path = criar_output_path
        self.__verificar_existencia_de_arquivo = verificar_existencia_de_arquivo

    def execute(self, credentials: dict, input_path: str, output_file_path: str) -> pd.DataFrame|list[str]:
        """ execute the processar dados brutos """
        dado_processado_path = output_file_path
        if not self.__verificar_existencia_de_arquivo.execute(dado_processado_path):
            stream_asset = self.__pdf_conversor.execute(credentials, input_path)
            dado_processado_path = self.__criar_output_path.execute(output_file_path, stream_asset)
        dados_processados = self.__ler_dados.execute(dado_processado_path)        

        return dados_processados
