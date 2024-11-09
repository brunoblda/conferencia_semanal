from project.use_cases.interfaces.transformar_arquivos.verificar_existencia_de_arquivo import VerificarExistenciaDeArquivo as VerificarExistenciaDeArquivoInterface
import os

class VerificarExistenciaDeArquivo(VerificarExistenciaDeArquivoInterface):
    """ Verifica se o arquivo existe """
    def execute(self, file_path: str) -> bool:
        """ Verifica se o arquivo existe """

        arquivo_existe = os.path.exists(file_path)

        return arquivo_existe