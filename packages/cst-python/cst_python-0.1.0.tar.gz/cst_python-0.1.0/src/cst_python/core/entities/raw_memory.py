import time
from typing import List, Optional, Any

from cst_python.python import alias
from .memory import Memory
from .memory_container import MemoryContainer
from .rest_memory_object import RESTMemoryObject
from .rest_memory_container import RESTMemoryContainer
from .memory_object import MemoryObject

#TODO createMemoryContainer, REST methods

class RawMemory:
    _last_id = 0

    def __init__(self) -> None:
        self._all_memories : List[Memory] = [] #Should be a set?
    
    #@alias.alias("getAllMemoryObjects", "get_all_memory_objects")
    @property
    def all_memories(self) -> List[Memory]:
        return self._all_memories
    
    #@alias.alias("setAllMemoryObjects", "set_all_memory_objects")
    @all_memories.setter
    def all_memories(self, value:List[Memory]) -> None:
        self._all_memories = value
        
        for m in self._all_memories:
            if m.get_id() is None:
                m.set_id(self._last_id)
                self._last_id += 1
    
    #@alias.alias("getAllOfType")
    def get_all_of_type(self, type:str) -> List[Memory]:
        list_of_type = []

        for m in self._all_memories:
            if m.compare_name(type):
                list_of_type.append(m)

        return list_of_type
    
    #@alias.alias("printContent")
    def print_content(self) -> None:
        for m in self._all_memories:
            print(m)

    #@alias.alias("addMemoryObject", "add_memory_object", "addMemory")
    def add_memory(self, m:Memory) -> None:
        self._all_memories.append(m)
        m.set_id(self._last_id)
        self._last_id += 1

    #@alias.alias("createMemoryContainer")
    def create_memory_container(self, name:str) -> MemoryContainer:
        raise NotImplementedError()
    
    #@alias.alias("createRESTMemoryObject")
    def create_rest_memory_object(self, name:str, port:int, hostname:Optional[str]=None) -> RESTMemoryObject:
        raise NotImplementedError()
    
    #@alias.alias("createRESTMemoryContainer")
    def create_rest_memory_container(self, name:str, port:int, hostname:Optional[str]=None) -> RESTMemoryContainer:
        raise NotImplementedError()
    
    #@alias.alias("createMemoryObject")
    def create_memory_object(self, name:str, info:Optional[Any]=None) -> MemoryObject:
        if info is None:
            info = ""
        
        mo = MemoryObject()

        mo.set_info(info)
        mo.timestamp = time.time()
        mo.set_evaluation(0.0)
        mo.set_name(name)

        self.add_memory(mo)
        return mo
    
    #@alias.alias("destroyMemoryObject", "destroy_memory_object")
    def destroy_memory(self, m:Memory):
        self._all_memories.remove(m)

    #@alias.alias("size")
    def __len__(self) -> int:
        return len(self._all_memories)
    
    #@alias.alias("shutDown", "shut_down")
    def shutdown(self) -> None:
        self._all_memories = []