import abc

from cst_python.python import alias

class MemoryObserver(abc.ABC):
    def __init__(self) -> None:
        raise NotImplementedError()
    
    #@alias.alias("notifyCodelet")
    @abc.abstractmethod
    def notify_codelet(self):
        raise NotImplementedError()