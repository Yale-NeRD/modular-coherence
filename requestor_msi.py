import inspect
import textwrap
from requestor_arch import requestor_arch
from requestor import requestor
from cache_state import *




class requestor_msi(requestor):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, requestor_arch, directory, local_cache_state):
		super(requestor_msi, self).__init__(requestor_arch, directory)


		#TODO: use function pointers (split function name with arguments) instead of strings 
		self.match_action_table[INVALID]["read"] = ["requestor_arch.send_request_to_network(self, self.directory, memory_addr, 'read')", 
													"requestor_arch.update_cache_state(self, memory_addr, 'mode', SHARED)"
														]
		self.match_action_table[INVALID]["write"] = ["requestor_arch.send_request_to_network(self, self.directory, memory_addr, 'write')", 
														"requestor_arch.update_cache_state(self,memory_addr, 'mode', MODIFIED)"
														]

		self.match_action_table[SHARED]["read"] = []
		self.match_action_table[SHARED]["write"] = ["requestor_arch.send_request_to_network(self, self.directory, memory_addr, 'write')", 
													  "requestor_arch.update_cache_state(self, memory_addr, 'mode', MODIFIED)"
														]

		self.match_action_table[MODIFIED]["read"] = []
		self.match_action_table[MODIFIED]["write"] = []


		self.local_cache_state = local_cache_state


	def get_cache_line_entry(self, memory_addr:int, requested_mode:str) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in (TODO: should be read, write)

		return:
		:data (str): the actual data from the cache line after it has been received
		'''


		cache_state = self.local_cache_state[memory_addr]
		for item in self.match_action_table[cache_state][requested_mode]:
			eval(item)

