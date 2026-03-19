from abc import ABC, abstractmethod

class BaseDriver(ABC):
    
    @abstractmethod
    def get_status(self):
        pass
    