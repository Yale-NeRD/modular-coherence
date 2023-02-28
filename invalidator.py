import inspect
import textwrap
from invalidator_arch import invalidator_arch
from cache_state import *

class invalidator(invalidator_arch):
	def __init__(self, name="a"):
		self.name = name


		for state in cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in cache_line_states:
				self.match_action_table[state][matched_state] = None


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



		pass

