from multiprocessing import Queue

from cst_python import use_memory_storage, create_memory_object, insert_codelet, start

from .common import PrintMessageCodelet, ChangeMessageCodelet

use_memory_storage(True)

msg = create_memory_object("message", "", ms=True) #Set the memory to use the MS
trigger = create_memory_object("trigger", False, ms=True) #Set the memory to use the MS

msg_queue = Queue()

codelet = PrintMessageCodelet(msg_queue)
codelet.add_input(msg)
codelet.add_input(trigger)
codelet.add_output(trigger) #Works in Java?

codelet2 = ChangeMessageCodelet("Python message")
codelet2.add_output(msg)
codelet2.add_output(trigger)

insert_codelet(codelet)
insert_codelet(codelet2)

start()

# Python print "Python message"

msg = msg_queue.get()
assert msg == "Python message"

# Start java code
...

# Java changes message and trigger=True
# Python prints "Java message"

msg = msg_queue.get()
assert msg == "Java message"