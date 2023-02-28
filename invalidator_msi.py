import inspect
import textwrap
from invalidator_arch import invalidator_arch
from cache_state import *
from invalidator import invalidator

class invalidator_msi(invalidator):
	def __init__(self, invalidator_arch, local_cache_state, name="a"):
		super(invalidator_msi, self).__init__(invalidator_arch, name)


		self.local_cache_state = local_cache_state


		self.match_action_table[SHARED][INVALID] = ["invalidator_arch.update_cache_line_state(self,memory_addr, 'mode', INVALID)"] 
		self.match_action_table[SHARED][SHARED] = [] 
		self.match_action_table[SHARED][MODIFIED] = []

		self.match_action_table[MODIFIED][INVALID] = ["invalidator_arch.flush_cache_line_entry_to_network(self,memory_addr)", 
														 "invalidator_arch.update_cache_line_state(self, memory_addr, 'mode', INVALID)"]
		self.match_action_table[MODIFIED][SHARED] = ["invalidator_arch.flush_cache_line_entry_to_network(self,memory_addr)", 
														 "invalidator_arch.update_cache_line_state(self,memory_addr, 'mode', SHARED)"]
		self.match_action_table[MODIFIED][MODIFIED] = []

	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		NONE
		'''

		cache_state = self.local_cache_state[memory_addr]
		for item in self.match_action_table[cache_state][new_mode]:
			eval(item)

		return 0

