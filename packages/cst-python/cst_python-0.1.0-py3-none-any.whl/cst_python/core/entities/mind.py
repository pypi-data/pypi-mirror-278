from typing import List, Dict, Optional, Any, Union

from cst_python.python import alias
from .code_rack import CodeRack
from .raw_memory import RawMemory
from .rest_memory_object import RESTMemoryObject
from .rest_memory_container import RESTMemoryContainer
from .memory_object import MemoryObject
from .codelet import Codelet
from .memory import Memory
from .memory_container import MemoryContainer

class Mind:
    def __init__(self) -> None:
        self._code_rack = CodeRack()
        self._raw_memory = RawMemory()
        self._codelet_groups : Dict[str, List[Codelet]] = dict()
        self._memory_groups : Dict[str, List[Memory]] = dict()

    #@alias.alias("getCodeRack", "get_code_rack")
    @property
    def code_rack(self) -> CodeRack:
        return self._code_rack

    #@alias.alias("getRawMemory", "get_raw_memory")
    @property
    def raw_memory(self) -> RawMemory:
        return self._raw_memory
    
    #@alias.alias("getCodeletGroups")
    @property
    def codelet_groups(self) -> Dict[str, List[Codelet]]:
        return self._codelet_groups

    #@alias.alias("getMemoryGroups")
    @property
    def memory_groups(self) -> Dict[str, List[Memory]]:
        return self._memory_groups

    #@alias.alias("createCodeletGroup")
    def create_codelet_group(self, group_name:str) -> None:
        self._codelet_groups[group_name] = []

    #@alias.alias("createMemoryGroup")
    def create_memory_group(self, group_name:str) -> None:
        self._memory_groups[group_name] = []

    #@alias.alias("getCodeletGroupsNumber")
    def get_codelet_groups_number(self) -> int:
        return len(self._memory_groups)

    #@alias.alias("getMemoryGroupsNumber")
    def get_memory_groups_number(self) -> int:
        return len(self._memory_groups)
    
    #@alias.alias("createMemoryContainer")
    def create_memory_container(self, name:str) -> Optional[MemoryContainer]:
        mc = None

        if self._raw is not None:
            mc = self._raw_memory.create_memory_container(name)

        return mc

    #@alias.alias("createRESTMemoryObject")
    def create_rest_memory_object(self, name:str, 
                                  port:int, 
                                  hostname:Optional[str]=None) -> Optional[RESTMemoryObject]:

        if hostname is None:
            hostname = "localhost"

        mo = None
        
        if self._raw_memory is not None:
            mo = self._raw_memory.create_rest_memory_object(name, hostname, port)

        return mo

    #@alias.alias("createRESTMemoryContainer")
    def create_rest_memory_container(self, name:str, 
                                     port:int, 
                                     hostname:Optional[str]=None) -> Optional[RESTMemoryContainer]:
        if hostname is None:
            hostname = "localhost"

        mc = None
        
        if self._raw_memory is not None:
            mc = self._raw_memory.create_rest_memory_container(name, hostname, port)

        return mc
    

    #@alias.alias("createMemoryObject")
    def create_memory_object(self, name:str, info:Optional[Any]=None) -> Optional[MemoryObject]:
        mo = None

        if self._raw_memory is not None:
            mo = self._raw_memory.create_memory_object(name, info)

        return mo
    
    #@alias.alias("insertCodelet")
    def insert_codelet(self, co:Codelet, group_name:Optional[str]=None) -> Codelet:
        if self._code_rack is not None:
            self._code_rack.add_codelet(co)

        self.register_codelet(co, group_name)

        return co
    
    #@alias.alias("registerCodelet")
    def register_codelet(self, co:Codelet, group_name:str) -> None:
        if group_name in self._codelet_groups:
            group_list = self._codelet_groups[group_name]
            group_list.append(co)
    
    #@alias.alias("registerMemory")
    def register_memory(self, memory:Union[Memory,str], group_name:str) -> None:

        if group_name in self._memory_groups:
            to_register = []
            
            if isinstance(memory, str) and self._raw_memory is not None:
                to_register += self._raw_memory.get_all_of_type(memory)
            else:
                to_register.append(memory)

            self._memory_groups[group_name] += to_register
    
    #@alias.alias("getCodeletGroupList")
    def get_codelet_group_list(self, group_name:str) -> List[Codelet]:
        return self._codelet_groups[group_name]
    
    #@alias.alias("getMemoryGroupList")
    def get_memory_group_list(self, group_name:str) -> List[Memory]:
        return self._memory_groups[group_name]
    
    def start(self) -> None:
        if self._code_rack is not None:
            self._code_rack.start()

    #@alias.alias("shutDown", "shut_down")
    def shutdown(self) -> None:
        if self._code_rack is not None:
            self._code_rack.shutdow()