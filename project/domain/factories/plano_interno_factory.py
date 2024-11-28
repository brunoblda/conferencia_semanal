from project.domain.entities.plano_interno import PlanoInterno
from project.domain.entities.plano_interno_seof import PlanoInternoSeof
from project.domain.entities.plano_interno_siafi import PlanoInternoSiafi
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.domain.interfaces.plano_interno_factory import PlanoInternoFactoryInterface


class PlanoInternoFactory(PlanoInternoFactoryInterface):
    def create(self, tipo: str) -> PlanoInternoInterface:
        if tipo == "pi_seof":
            return PlanoInternoSeof()
        elif tipo == "pi_siafi":
            return PlanoInternoSiafi()
        elif tipo == "pi":
            return PlanoInterno()
