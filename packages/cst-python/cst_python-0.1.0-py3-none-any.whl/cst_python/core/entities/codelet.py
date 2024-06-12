from __future__ import annotations

import abc
import traceback
import threading
import time
from typing import List, Optional

from cst_python.python import alias
from .memory import Memory
from .memory_buffer import MemoryBuffer

#TODO: Profile, Broadcast, impending access, correct exception types

#@alias.aliased
class Codelet(abc.ABC):

    def __init__(self) -> None:
        self._threshold = 0.0
        self._inputs : List[Memory] = []
        self._outputs : List[Memory] = []
        self._broadcast : List[Memory] = []
        self._loop = True
        self._is_memory_observer = False
        self._time_step = 300
        self._enabled = True
        self._enable_count = 0
        self._name = threading.currentThread().name
        self._last_start_time = 0.0
        self._lock = threading.RLock()
        self._activation = 0.0
        #self._timer = 
        self._is_profiling = False
        self._thread : threading.Thread = None
        self._codelet_profiler = None
        self._additional_wait = 0.0



    
    #@alias.alias("should_loop", "shouldLoop", "is_loop", "isLoop")
    @property
    def loop(self) -> bool:
        return self._loop

    #@alias.alias("set_loop", "setLoop")
    @loop.setter
    def loop(self, value) -> None:
        self._loop = value

    #@alias.alias("get_enabled", "getEnabled")
    @property
    def enabled(self) -> bool:
        return self._enabled
    
    #@alias.alias("set_enabled", "setEnabled")
    @enabled.setter
    def enabled(self, value:bool) -> None:
        self._enabled = value

        if self._enabled:
            self._enable_count = 0

    #@alias.alias("get_name", "getName")
    @property
    def name(self) -> str:
        return self._name

    #@alias.alias("set_name", "setName")
    @name.setter
    def name(self, value:str) -> None:
        self._name = value

    #@alias.alias("get_activation", "getActivation")
    @property
    def activation(self) -> float:
        return self._activation
    
    #@alias.alias("set_activation", "setActivation")
    @activation.setter
    def activation(self, value:float):
        if value > 1.0 or value < 0.0:
            raise ValueError(f"Codelet activation must be in (0.0 , 1.0) \
                             (value {value} is not allowed).")
        
        self._activation = value

    #@alias.alias("get_inputs", "getInputs")
    @property
    def inputs(self) -> List[Memory]:
        return self._inputs
    
    #@alias.alias("set_inputs", "setInputs")
    @inputs.setter
    def inputs(self, value:List[Memory]):
        self._inputs = value

    #@alias.alias("get_outputs", "getOutputs")
    @property
    def outputs(self) -> List[Memory]:
        return self._outputs

    #@alias.alias("set_outputs", "setOutputs")
    @outputs.setter
    def outputs(self, value:List[Memory]):
        self._outputs = value

    #@alias.alias("get_threshould", "getThreshould")
    @property
    def threshould(self) -> float:
        return self._threshold

    #@alias.alias("set_threshould", "setThreshould")
    @threshould.setter
    def threshould(self, value:float):
        if value > 1.0 or value < 1.0:
            raise ValueError(f"Codelet threshould must be in (0.0 , 1.0) \
                             (value {value} is not allowed).")
        
        self._threshold = value

    #@alias.alias("get_time_step", "getTime_step")
    @property
    def time_step(self) -> float:
        return self._time_step

    #@alias.alias("set_time_step", "setTime_step")
    @time_step.setter
    def time_step(self, value:float):
        
        self._time_step = value

    #@alias.alias("get_broadcast", "getBroadcast")
    #Problem: get_broadcast method overload
    @property
    def broadcast(self) -> List[Memory]:
        return self._broadcast

    #@alias.alias("set_broadcast", "setBroadcast")
    @broadcast.setter
    def broadcast(self, value:List[Memory]) -> None:
        self._broadcast = value

    #@alias.alias("IsProfiling")
    @property
    def is_profiling(self) -> bool:
        return self._is_profiling

    #@alias.alias("set_profiling", "setProfiling")
    @is_profiling.setter
    def is_profiling(self, value:bool):
        if value is True:
            raise NotImplementedError("Profiling is not implemented")

        self._is_profiling = value

    @property
    def is_memory_observer(self) -> bool:
        return self._is_memory_observer
    
    @is_memory_observer.setter
    def is_memory_observer(self, value) -> None:
        self._is_memory_observer = value

    ##########################################################################


    #@alias.alias("accessMemoryObjects")
    @abc.abstractmethod
    def access_memory_objects(self) -> None:
        ...
    
    #@alias.alias("calculateActivation")
    @abc.abstractmethod
    def calculate_activation(self) -> None:
        ...

    @abc.abstractmethod
    def proc(self) -> None:
        ...

    def run(self) -> None:

        try:
            self._scheduled_run()
        except Exception as e:
            traceback.print_exception(e)

    def start(self) -> None:
        thread = threading.Thread(target=self.run, daemon=True)
        self._thread = thread

        thread.start()
        #thread.join(0.0)

        

    def stop(self):
        self.loop = False
        self._thread.join(0.0)

    #@alias.alias("impendingAccess")
    def impending_acess(self, accessing:Codelet) -> bool:
        raise NotImplementedError()

    #@alias.alias("impendingAccessBuffer")
    def impending_access_buffer(self, accessing:MemoryBuffer) -> bool:
        raise NotImplementedError()
    
    #@alias.alias("addInput")
    def add_input(self, memory:Memory) -> None:
        if self._is_memory_observer:
            memory.add_memory_observer(self)
        
        self._inputs.append(memory)

    #@alias.alias("addInputs")
    def add_inputs(self, memories:List[Memory]) -> None:
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._inputs += memories

    #@alias.alias("addOutput")
    def add_output(self, memory:Memory) -> None:
        self._outputs.append(memory)

    #@alias.alias("removesOutput")
    def removes_output(self, memory:Memory) -> None:
        self._outputs.remove(memory)

    #@alias.alias("removesInput")
    def removes_input(self, memory:Memory) -> None:
        self._inputs.remove(memory)

    #@alias.alias("removeFromOutput")
    def remove_from_output(self, memories:List[Memory]) -> None:
        self._outputs = [m for m in self._outputs if m not in memories]

    #@alias.alias("removeFromInput")
    def remove_from_input(self, memories:List[Memory]) -> None:
        self._inputs = [m for m in self._inputs if m not in memories]

    #@alias.alias("addOutputs")
    def add_outputs(self, memories:List[Memory]) -> None:
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._outputs += memories

    #@alias.alias("getOutputsOfType")
    def get_outputs_of_type(self, type:str) -> List[Memory]:
        outputs_of_type = []

        if self._outputs is not None:
            for m in self._outputs:
                if m.compare_name(type):
                    outputs_of_type.append(m)

        return outputs_of_type

    #@alias.alias("getInputsOfType")
    def get_inputs_of_type(self, type:str) -> List[Memory]:
        inputs_of_type = []

        if self._inputs is not None:
            for m in self._inputs:
                if m.compare_name(type):
                    inputs_of_type.append(m)

        return inputs_of_type

    #@alias.alias("getBroadcast")
    def get_broadcast(self, name:str) -> Memory:
        if self._broadcast is not None:
            for m in self._broadcast:
                if m.compare_name(name):
                    return m

    #@alias.alias("addBroadcast")
    def add_broadcast(self, memory:Memory) -> None:
        if self._is_memory_observer:
            memory.add_memory_observer(self)
        
        self._broadcast.append(memory)

    #@alias.alias("addBroadcasts")
    def add_broadcasts(self, memories:List[Memory]) -> None:
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._broadcast += memories


    #@alias.alias("getThreadName")
    def get_thread_name(self) -> str:
        return threading.currentThread().name
    
    #@alias.alias("to_string", "toString")
    def __str__(self) -> str:
        max_len = 10

        result = f"Codelet [activation={self._activation}, name={self._name}, "

        if self._broadcast is not None:
            result += self._broadcast[min(len(self._broadcast), max_len)]
            result += ", "
        
        if self._inputs is not None:
            result += self._inputs[min(len(self._outputs), max_len)]
            result += ", "

        if self._outputs is not None:
            result += self._outputs[min(len(self._outputs), max_len)]
            result += ", "
        
        result += "]"

        return result
    
    def _get_memory(self, search_list:List[Memory], type:Optional[str]=None, 
                    index:Optional[int]=None, name:Optional[str]=None) -> Memory:

        found_MO = None

        if type is not None and index is not None:
            list_MO :List[Memory] = []

            if search_list is not None:
                for m in search_list:
                    if m.compare_name(type):
                        list_MO.append(m)

            if len(list_MO) >= index+1:
                found_MO = list_MO[index]        

        elif name is not None:
            for m in search_list:
                if m.compare_name(name):
                    found_MO = m
                    break

        if found_MO is None:
            self._enabled = False
            self._enable_count += 1
        else:
            self.enabled = True

        return found_MO

    #@alias.alias("getInput")
    def get_input(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory:
        return self._get_memory(self._inputs, type, index, name)

    #@alias.alias("getOutput")
    def get_output(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory:
        return self._get_memory(self._outputs, type, index, name)

    #@alias.alias("getBroadcast")
    def get_broadcast(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory:
        return self._get_memory(self._broadcast, type, index, name)

    
    #@alias.alias("setPublishSubscribe")
    def set_publish_subscribe(self, enable:bool) -> None:
        if enable:
            self.is_memory_observer = True

            for m in self._inputs:
                m.add_memory_observer(self)

        else:
            for m in self._inputs:
                m.remove_memory_observer(self)

            self.is_memory_observer = False

            try:
                self._additional_wait += 300
            except Exception:
                pass

            self.run()


    #@alias.alias("setCodeletProfiler")
    def set_codelet_profiler(self, *args, **kargs) -> None:
        raise NotImplementedError()
    

    #@alias.alias("raiseException")
    def _raise_exception(self) -> None:
        raise RuntimeError(f"This codelet could not find a memory object it needs: {self.name}")

    #@alias.alias("notifyCodelet")
    def notify_codelet(self) -> None:
        try:
            if self._is_profiling:
                start_time = time.time()
            
            self.access_memory_objects()

            if self._enable_count == 0:
                self.calculate_activation()

                if self.activation >= self.threshould:
                    self.proc()
            else:
                self._raise_exception()

        except Exception as e:
            #Logging
            pass
        
        finally:
            if self._codelet_profiler is not None:
                self._codelet_profiler.profile(self)
            
            if self._is_profiling:
                end_time = time.time()
                duration = (end_time-start_time)

                #TODO profiling


    def _scheduled_run(self):
        run = True

        while run:
            run = False

            start_time = 0.0
            end_time = 0.0
            duration = 0.0

            try:
                if not self._is_memory_observer:
                    self.access_memory_objects()
                
                if self._enable_count == 0:
                    if not self._is_memory_observer:
                        self.calculate_activation()

                        if self._activation >= self._threshold:
                            self.proc()

                else:
                    self._raise_exception()

            
            except Exception as e:
                traceback.print_exception(e)
                #logging
                pass

            finally:
                if not self._is_memory_observer and self._loop:
                    run = True
                
                #Profiling

            if run:
                #Not right, must wait anytime
                time_to_sleep = self._additional_wait + self._time_step
                time_to_sleep /= 1000 #ms to s
                time.sleep(time_to_sleep)