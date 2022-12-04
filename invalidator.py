import inspect
import textwrap
from invalidator_arch import invalidator_arch

# ###STATE DEFINITIONS###
# MODIFIED = 2
# SHARED = 1
# INVALID = 0


class invalidator(invalidator_arch):
	def __init__(self):
		cache_entry_states = {
			"modified":2,
			"shared":1,
			"invalid":0
			}


	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		TODO
		'''
		if data_required:
			self.flush_page_to_network(memory_addr)
		if remove_data == True:
			self.update_cache_state(cache_line, "mode", 0)
		if remove_data == False:
			self.update_cache_state(cache_line, "mode", 1)




###DO NOT CHANGE BELOW THIS