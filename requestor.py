import inspect
import textwrap
from requestor_arch import requestor_arch

#GLOBAL STATE DEFINTIONS
MODIFIED = 2
SHARED = 1 
INVALID = 0


class requestor(requestor_arch):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, directory):

		self.valid_requestor_mode_transitions =  {
			0: [1,2],
			1: [1,2],
			2: [2]
		}
		#keys are what is stored in the cache controller 
		#values are correct transition states for the cache controller 

		self.number_of_states = 3 #n
		self.cache_line_states = ["invalid", "shared", "modified"]

		#make a table of size n x n states
		self.match_action_table = {}

		self.cache_state = {}
		#key = memory_addr
		#value = cache state/mode

		self.directory = directory



		#TODO: do i need to define state to allowed permission (i.e. S-> read, I--> none, M-->read,write)


	def get_cache_line_entry(self, memory_addr:int, requested_mode:str) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in (TODO: should be read, write)

		return:
		:data (str): the actual data from the cache line after it has been received
		'''


		for state in self.cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in self.cache_line_states:
				self.match_action_table[state][matched_state] = None


		#TODO: use function pointers (split function name with arguments) instead of strings 
		self.match_action_table["invalid"]["read"] = ["self.send_request_to_network(memory_addr, 'read')", 
														"self.update_cache_state(memory_addr, 'mode', 'shared')"
														]
		self.match_action_table["invalid"]["write"] = ["self.send_request_to_network(memory_addr, 'write')", 
														"self.update_cache_state(memory_addr, 'mode', 'modified')"
														]

		self.match_action_table["shared"]["read"] = ["ERROR"]
		self.match_action_table["shared"]["write"] = ["self.send_request_to_network(memory_addr, 'write')", 
													  "self.update_cache_state(memory_addr, 'mode', 'modified')"
														]

		self.match_action_table["modified"]["read"] = ["ERROR"]
		self.match_action_table["modified"]["write"] = ["ERROR"]


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



