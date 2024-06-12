import traceback
from typing import List

from cst_python.python import alias
from .codelet import Codelet
from .memory import Memory


class CodeRack:
    def __init__(self) -> None:
        self._all_codelets :List[Codelet] = []

    #@alias.alias("getAllCodelets", "get_all_codelets")
    @property
    def all_codelets(self) -> List[Codelet]:
        return self._all_codelets

    #@alias.alias("setAllCodelets", "set_all_codelets")
    @all_codelets.setter
    def all_codelets(self, value:List[Codelet]) -> None:
        self._all_codelets = value

    #@alias.alias("add_codelet")
    def add_codelet(self, codelet:Codelet) -> None:
        self._all_codelets.append(codelet)

    #@alias.alias("insertCodelet")
    def insert_codelet(self, codelet:Codelet) -> Codelet:
        self.add_codelet(codelet)

        return codelet
    
    #@alias.alias("createCodelet")
    def create_codelet(self, activation:float, broadcast:List[Memory],
                       inputs:List[Memory], outputs:List[Memory],
                       codelet:Codelet) -> Codelet:
        
        try:
            codelet.activation = activation
        except Exception as e:
            traceback.print_exception(e)

        codelet.broadcast = broadcast
        codelet.inputs = inputs
        codelet.outputs = outputs

        self.add_codelet(codelet)

        return codelet
    
    #@alias.alias("destroyCodelet")
    def destroy_codelet(self, codelet:Codelet) -> None:
        codelet.stop()
        self._all_codelets.remove(codelet)

    #@alias.alias("shutDown", "shut_down")
    def shutdow(self):
        self.stop()
        self._all_codelets.clear()

    def start(self) -> None:
        for codelet in self._all_codelets:
            codelet.start()

    def stop(self) -> None:
        for codelet in self._all_codelets:
            codelet.stop()
