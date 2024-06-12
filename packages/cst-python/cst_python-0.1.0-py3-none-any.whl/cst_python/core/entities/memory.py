import abc
from typing import Any

from cst_python.python import alias
from.memory_observer import MemoryObserver

class Memory(abc.ABC):
    
    #@alias.alias("getI", "get_I")
    @abc.abstractmethod
    def get_info(self) -> Any:
        ...
    
    #@alias.alias("setT", "set_I")
    @abc.abstractmethod
    def set_info(self, value:Any) -> int:
        ...

    #@alias.alias("getEvaluation")
    @abc.abstractmethod
    def get_evaluation(self) -> float:
        ...

    #@alias.alias("getName")
    @abc.abstractmethod
    def get_name(self) -> str:
        ...

    #@alias.alias("setName")
    @abc.abstractmethod
    def set_name(self, name:str) -> None:
        ...

    #@alias.alias("setEvaluation")
    @abc.abstractmethod
    def set_evaluation(self, evaluation:float) -> None:
        ...

    #@alias.alias("getTimestamp")
    @abc.abstractmethod
    def get_timestamp(self) -> float:
        ...

    #@alias.alias("addMemoryObserver")
    @abc.abstractmethod
    def add_memory_observer(self, observer:MemoryObserver) -> None:
        ...

    #@alias.alias("removeMemoryObserver")
    @abc.abstractmethod
    def remove_memory_observer(self, observer:MemoryObserver) -> None:
        ...

    #@alias.alias("getId")
    @abc.abstractmethod
    def get_id(self) -> float:
        ...

    #@alias.alias("setId")
    @abc.abstractmethod
    def set_id(self, memory_id:float) -> None:
        ...

    #@alias.alias("getTimestamp")
    @abc.abstractmethod
    def get_timestamp(self) -> float:
        ...
    

    def compare_name(self, other_name:str) -> bool:
        if self._name is None:
            return False
        
        return self._name.lower() == other_name.lower()
    