import inspect
import textwrap
from invalidator_arch import invalidator_arch

###STATE DEFINITIONS###
MODIFIED = 2
SHARED = 1
INVALID = 0

class invalidator(invalidator_arch):
	def __init__(self, name="random_name"):
		self.valid_requestor_mode_transitions = {
			0: [],
			1: [0],
			2: [0,1]
		}
		#keys are what is stored in the cache controller 
		#values are correct transition states for the cache controller 
		self.name = name

		self.number_of_states = 3 #n
		self.cache_line_states = ["invalid", "shared", "modified"]

		#make a table of size n x n states
		self.match_action_table = {}

		self.cache_state = {}
		#key = memory_addr
		#value = cache state/mode

	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		NONE
		'''

		for state in self.cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in self.cache_line_states:
				self.match_action_table[state][matched_state] = None


		self.match_action_table["shared"]["invalid"] = ["self.update_cache_line_state(memory_addr, 'mode', 'invalid')"] #TODO figure out if I have to delete the data as well
		self.match_action_table["shared"]["shared"] = ["ERROR"] 
		self.match_action_table["shared"]["modified"] = ["ERROR"]

		self.match_action_table["modified"]["invalid"] = ["self.flush_cache_line_entry_to_network(memory_addr)", 
														 "self.update_cache_line_state(memory_addr, 'mode', 'invalid')"]
		self.match_action_table["modified"]["shared"] = ["self.flush_cache_line_entry_to_network(memory_addr)", 
														 "self.update_cache_line_state(memory_addr, 'mode', 'shared')"]
		self.match_action_table["modified"]["modified"] = ["ERROR"]


		local_cache_state = self.cache_state[memory_addr]
		for item in self.match_action_table[local_cache_state][new_mode]:
			if item == "ERROR":
				print(item)
				break
			print("invalidator_"+self.name+"_"+item)

		return 0

