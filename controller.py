import inspect
import textwrap
from requestor_msi import requestor_msi
from invalidator_msi import invalidator_msi
from directory_msi import directory_msi
from cache_state import *
from requestor_arch import requestor_arch
from directory_arch import directory_arch
from invalidator_arch import invalidator_arch


class controller(object):
	def __init__(self, requestor, invalidator, directory, requestor_arch,invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
		self.requestor = requestor(requestor_arch, directory, requestor_cache_state)
		self.invalidator = invalidator(invalidator_arch, invalidator_cache_state, name)


#initialize all architectures 
requestor_arch1 = requestor_arch()
invalidator_arch1 = invalidator_arch()
dir_arch = directory_arch()
directory = directory_msi(dir_arch)


#initialize initial block states
shared_state = {0:INVALID}
shared_state2 = {0:MODIFIED}


#two controllers that have requestor and invalidator
a1 = controller(requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1,shared_state, shared_state, name="a1")
a2 = controller(requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1, shared_state2, shared_state2, name="a2")

#directory state
directory.global_cache_state[0] = {"data":0, "mode": MODIFIED, "sharers": [a2]}

#request by one controller to a cache line entry
a1.requestor.get_cache_line_entry(0, "write")

