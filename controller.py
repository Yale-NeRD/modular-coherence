import inspect
import textwrap
from requestor_msi import requestor_msi
from invalidator_msi import invalidator_msi
from directory_msi import directory_msi
from cache_state import *
from requestor_arch import requestor_arch


class controller(object):
	def __init__(self, requestor, invalidator, directory, requestor_arch,requestor_cache_state, invalidator_cache_state, name):
		self.requestor = requestor(requestor_arch, directory, requestor_cache_state)
		self.invalidator = invalidator(invalidator_cache_state, name)


requestor_arch1 = requestor_arch()
shared_state = {0:INVALID}
directory = directory_msi()
a1 = controller(requestor_msi, invalidator_msi, directory, requestor_arch1, shared_state, shared_state, name="a1")


shared_state2 = {0:MODIFIED}
a2 = controller(requestor_msi, invalidator_msi, directory, requestor_arch1, shared_state2, shared_state2, name="a2")





directory.global_cache_state[0] = {"data":0, "mode": MODIFIED, "sharers": [a2]}
a1.requestor.get_cache_line_entry(0, "write")

