import inspect
import textwrap
from requestor_arch import requestor_arch
from cache_state import *


class requestor(object):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, interconnect, requestor_arch,directory, name):

		requestor_arch = requestor_arch

		self.match_action_table = {}

		self.name = name

		for state in cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in cache_line_states:
				self.match_action_table[state][matched_state] = None


		self.directory = directory

		self.interconnect = interconnect
		self.requestor_queue = self.interconnect.controller_queues[self.name]["requestor"]

		# self.local_cache_state = {}


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





