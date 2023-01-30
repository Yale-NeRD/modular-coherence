import inspect
import textwrap
from invalidator_arch import invalidator_arch

###STATE DEFINITIONS###
MODIFIED = 2
SHARED = 1
INVALID = 0

class invalidator(invalidator_arch):
	def __init__(self):
		self.valid_requestor_mode_transitions = 
		{
			0: []
			1: [0]
			2: [0,1]
		}
		#keys are what is stored in the cache controller 
		#values are correct transition states for the cache controller 

	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		TODO
		'''
		stored_cache_line_mode = self.get_stored_cache_line_mode(memory_addr)

		if stored_cache_line_mode == MODIFIED and new_mode == SHARED:
			self.flush_cache_line_entry_to_network(memory_addr)
			self.update_cache_line_state(memory_addr, "mode", 1)
		elif stored_cache_line_mode == MODIFIED and new_mode == INVALID:
			self.flush_cache_line_entry_to_network(memory_addr)
			self.update_cache_line_state(memory_addr, "mode", 0)
		elif stored_cache_line_mode == SHARED and new_mode == INVALID:
			self.update_cache_line_state(memory_addr, "mode", 0)
		else:
