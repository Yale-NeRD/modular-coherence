import inspect
import textwrap
from invalidator_arch import invalidator_arch
from cache_state import *
from invalidator import invalidator

class invalidator_msi(invalidator):
	def __init__(self, local_cache_state, name="a"):
		super(invalidator_msi, self).__init__(name)


		self.local_cache_state = local_cache_state


		print("invalidator match action table", self.match_action_table)

		self.match_action_table[SHARED]["invalid"] = ["self.update_cache_line_state(memory_addr, 'mode', 'invalid')"] #TODO figure out if I have to delete the data as well
		self.match_action_table[SHARED]["shared"] = ["ERROR"] 
		self.match_action_table[SHARED]["modified"] = ["ERROR"]

		self.match_action_table[MODIFIED]["invalid"] = ["self.flush_cache_line_entry_to_network(memory_addr)", 
														 "self.update_cache_line_state(memory_addr, 'mode', 'invalid')"]
		self.match_action_table[MODIFIED]["shared"] = ["self.flush_cache_line_entry_to_network(memory_addr)", 
														 "self.update_cache_line_state(memory_addr, 'mode', 'shared')"]
		self.match_action_table[MODIFIED]["modified"] = ["ERROR"]

	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		NONE
		'''

		# print(local_state_state)
		cache_state = self.local_cache_state[memory_addr]
		for item in self.match_action_table[cache_state][new_mode]:
			if item == "ERROR":
				print(item)
				break
			print("invalidator_"+self.name+"_"+item)

		return 0

