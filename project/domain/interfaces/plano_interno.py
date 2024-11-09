from abc import ABC, abstractmethod

class PlanoInterno(ABC):
    @abstractmethod
    def set(self, plano_interno):
        """ set the plano interno """
        raise NotImplementedError('Method not implemented')
    
    @abstractmethod
    def set_dict(self, dict_plano_interno):
        """ set the dict plano interno """
        raise NotImplementedError('Method not implemented')
    
    @abstractmethod
    def get_dict(self):
        """ get the dict plano interno """
        raise NotImplementedError('Method not implemented')
    
    @abstractmethod
    def get(self):
        """ get the plano interno """
        raise NotImplementedError('Method not implemented')
