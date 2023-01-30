import inspect
import textwrap
from requestor_arch import requestor_arch

#GLOBAL STATE DEFINTIONS
MODIFIED = 2
SHARED = 1 
INVALID = 0


class requestor(requestor_arch):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self):

		self.valid_requestor_mode_transitions = 
		{
			0: [1,2]
			1: [1,2]
			2: [2]
		}
		#keys are what is stored in the cache controller 
		#values are correct transition states for the cache controller 
	def get_cache_line_entry(self, memory_addr:int, requested_mode:int) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in

		return:
		:data (str): the actual data from the cache line after it has been received
		'''

		##commands that are always done##
		self.initialize_cache_line_entry(memory_addr)
		stored_cache_line_mode = self.get_stored_cache_line_mode(memory_addr)
		self.verify_state_transition_validity(stored_cache_line_mode, requested_mode)

		

		##commands that can be modified by the cache coherence developer##
		if stored_cache_line_mode == MODIFIED:
			return self.get_data_from_cache_line(memory_addr)
		elif stored_cache_line_mode == SHARED and requested_mode == MODIFIED:
			self.send_request_to_network(memory_addr, requested_mode) #mode may be M, S, E, etc. 
		elif stored_cache_line_mode == INVALID and (requested_mode == MODIFIED or requested_mode == SHARED):
			self.send_request_to_network(memory_addr, requested_mode)
		else:
			return ERROR

		self.update_cache_state(memory_addr, "mode", requested_mode)
		return self.get_data_from_cache_line(memory_addr)


	def verify_state_transition_validity(self, start_mode, end_mode):
		if start_mode in self.valid_requestor_mode_transitions and end_mode in self.valid_requestor_mode_transitions[start_mode]:
			return True
		return False
