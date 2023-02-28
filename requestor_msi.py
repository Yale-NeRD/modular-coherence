import inspect
import textwrap
from requestor_arch import requestor_arch
from requestor import requestor
from cache_state import *




class requestor_msi(requestor):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, directory):
		super(requestor_msi, self).__init__(directory, local_cache_state)


		#TODO: use function pointers (split function name with arguments) instead of strings 
		self.match_action_table[INVALID]["read"] = ["self.send_request_to_network(memory_addr, 'read')", 
														"self.update_cache_state(memory_addr, 'mode', 'shared')"
														]
		self.match_action_table[INVALID]["write"] = ["self.send_request_to_network(memory_addr, 'write')", 
														"self.update_cache_state(memory_addr, 'mode', 'modified')"
														]

		self.match_action_table[SHARED]["read"] = ["ERROR"]
		self.match_action_table[SHARED]["write"] = ["self.send_request_to_network(memory_addr, 'write')", 
													  "self.update_cache_state(memory_addr, 'mode', 'modified')"
														]

		self.match_action_table[MODIFIED]["read"] = ["ERROR"]
		self.match_action_table[MODIFIED]["write"] = ["ERROR"]





	def get_cache_line_entry(self, memory_addr:int, requested_mode:str) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in (TODO: should be read, write)

		return:
		:data (str): the actual data from the cache line after it has been received
		'''



		cache_state = self.cache_state[memory_addr]
		for item in self.match_action_table[cache_state][requested_mode]:
			if item == "ERROR":
				print(item)
				break
			print("requestor_"+item)
			eval(item)


	def send_request_to_network(self,address:int, mode:str) -> int: #is_read can just be mode (eg. M, O, E, S,...)
		'''
		request cache line from network 

		params:
		:address - address of page desired 
		:mode (int) - request of M, O, E, S, I, etc. (should map to cache_entry_states)

		
		return:
		: mode: mode of address being returned 

		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		1. send cache line request for new mode (if needed) to the directory 
		2. Wait for response from directory before returning, which is packet that has 
		information about data and new_mode to change local state to 
		3. add data (if received) to local cache controller 

		'''
		self.directory.collect_and_respond_requests(address, mode)


		return True



