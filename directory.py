import inspect
import textwrap
from cache_state import *


class directory(object):
	def __init__(self):

		self.cache_line_states = ["invalid", "shared", "modified"]

		#make a table of size n x n states
		self.match_action_table = {}

		for state in cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in cache_line_states:
				self.match_action_table[state][matched_state] = None

		self.global_cache_state = {}
		#key = cache_addr
		#value = dict(data, mode, [sharers])

	def collect_and_respond_requests(self, memory_addr:int, requested_mode:int) -> int:
		'''

		params:
		:memory_addr - address of requested block
		:requested_mode - new permissions mode for the requested block

		return:
		NONE
		'''


		pass


	def invalidate_sharers(self, memory_addr, new_mode):

		pass 




