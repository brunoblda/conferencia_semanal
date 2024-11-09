from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.domain.interfaces.plano_interno_factory import PlanoInternoFactoryInterface

class PlanoInternoFactory(PlanoInternoFactoryInterface):
    def create(self) -> PlanoInternoInterface:
        return PlanoInternoInterface()