import inspect
import textwrap
from requestor_arch import requestor_arch


###STATE DEFINITIONS###
# MODIFIED = 2
# SHARED = 1
# INVALID = 0


class requestor(requestor_arch):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self):
		cache_entry_states = {
		"modified":2,
		"shared":1,
		"invalid":0
		}

	def get_cache_line_entry(self, memory_addr:int, requested_mode:int) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in

		return:
		:data (str): the actual data from the cache line after it has been received

		'''
		stored_cache_line_mode = self.get_stored_cache_line_mode(memory_addr)

		if stored_cache_line_mode == MODIFIED:
			return self.get_data_from_cache_line(memory_addr)
	
		self.initialize_cache_entry(memory_addr)

		if stored_cache_line_mode == SHARED and requested_mode != SHARED :
			self.send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
		if stored_cache_line_mode == INVALID:
			self.send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
		elif hi:
			pass

		self.update_cache_state(memory_addr, "mode", requested_mode)
		return self.get_data_from_cache_line(memory_addr)






'''
note for any given simple cache coherence protocol there are three options:
	1. read --> write
	2. invalid --> read
	3. invalid --> write
'''