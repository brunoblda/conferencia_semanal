from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface


class PlanoInterno(PlanoInternoInterface):

    def set(self, plano_interno: list) -> None:
        self.plano_interno: list = plano_interno

    def set_dict(self, dict_plano_interno: dict) -> None:
        self.dict_plano_interno: dict = dict_plano_interno

    def get_dict(self) -> dict:
        return self.dict_plano_interno

    def get(self) -> list:
        return self.plano_interno
