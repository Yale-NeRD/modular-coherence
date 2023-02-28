import inspect
import textwrap
from requestor_arch import requestor_arch
from cache_state import *


class requestor(requestor_arch):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, directory):

		for state in cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in cache_line_states:
				self.match_action_table[state][matched_state] = None

		# self.number_of_states = 3 #n
		# self.cache_line_states = ["invalid", "shared", "modified"]

		# #make a table of size n x n states
		# self.match_action_table = {}

		# #key = memory_addr
		# #value = cache state/mode

		self.directory = directory


	def get_cache_line_entry(self, memory_addr:int, requested_mode:str) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in (TODO: should be read, write)

		return:
		:data (str): the actual data from the cache line after it has been received
		'''


		pass





