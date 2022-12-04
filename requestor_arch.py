class requestor_arch(object):
	def __init__(self):
		cache_entry_states = {
			"modified":2,
			"shared":1,
			"invalid":0
			}
	def get_data_from_cache_line(self, memory_addr: int) -> str:
		'''
		after knowing that the data exists, 
		return the data that is in the cache line for the processor's use. 
		
		params:
		:memory_addr (int) -  memory address of requested cache line 

		return:
		:data (str): the actual data from the cache_line

		'''
		pass

	def get_stored_cache_line_mode(self, memory_addr: int) -> int:
		'''
		gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
		if cache line entry doesn't exist: return invalid)

		params:
		:memory_addr -  memory address of requested cache line 

		return:
		:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I)

		'''
		return mode

		'''
		expected semantics for architecture developer:
			 - ensure that address exists in cache
		'''

	def initialize_cache_entry(self,memory_addr:int) -> int: #
		'''
		prepares a cache_entry before a request is made. Specifically, if:
			- If cache entry doesn't exist for address, prepare cache entry for it (i.e. evict block)
			- If cache entry exists, return True
			- other cases error out (return False)

		params:
		:memory_addr - memory address of data being requested

		No return value
		'''
		return None

		'''
		expected semantics for architecture developer:
			 - do same thing in description above 
		'''


	def send_request_to_network(self,address:int, mode:int) -> int: #is_read can just be mode (eg. M, O, E, S,...)
		'''
		request cache line from network 

		params:
		:address - address of page desired 
		:mode (int) - request of M, O, E, S, I, etc. (should map to cache_entry_states)

		
		return:
		: mode: mode of address being returned 
		'''
		pass
		# return response #from network  

		'''
		expected semantics for architecture developer:
			 - send request to network (i.e. the network RDMA)
		'''


	def update_cache_state(self, memory_addr:int, state:str, new_value:int) -> int:
		'''
		update cache line to a new_state (generally after response from network)

		params:
		:memory_addr - address of requested block of data 
		:state - state that is being updated
		:new_value - new value for state
		'''

		'''
		expected semantics for architecture developer:
			- The code needs to figure out the cache entry for the memory_addr
			- Then for the given state, must update the value (i.e. the mode may change from S --> M or I-->S)
		'''
		pass