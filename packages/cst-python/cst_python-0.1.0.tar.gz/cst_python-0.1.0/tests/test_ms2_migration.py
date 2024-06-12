import time
from multiprocessing import Queue

from cst_python import use_memory_storage, create_memory_object, insert_codelet, start

from .common import PrintMessageCodelet, ChangeMessageCodelet

use_memory_storage(True)

msg_memory = create_memory_object("message", "") #The memory location starts in the Python
trigger = create_memory_object("trigger", False, ms=True) #Starts the memory on the MS, for avoiding later copy

msg_queue = Queue()

codelet = PrintMessageCodelet(msg_queue)
codelet.add_input(msg_memory)
codelet.add_input(trigger)
codelet.add_output(trigger) #Works in Java?

codelet2 = ChangeMessageCodelet("Python message")
codelet2.add_output(msg_memory)
codelet2.add_output(trigger)

insert_codelet(codelet)
insert_codelet(codelet2)

start()

# Python print "Python message"
msg = msg_queue.get()
assert msg == "Python message"

# Start java code
...

# Java see message and trigger on the MS registry, migrate message to MS as it will be used in another node 
# Python memories are migrated to the MS
# Codelets run "access_memory_objects" again as previous memories was invalidated?
# Java changes message and trigger=True

# Python prints "Java message"

msg = msg_queue.get()
assert msg == "Java message"