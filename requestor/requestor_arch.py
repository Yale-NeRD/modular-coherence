#GLOBAL STATE DEFINTIONS
MODIFIED = 2
SHARED = 1 
INVALID = 0

class requestor_arch(object):
	def __init__(self):
		pass

	def get_data_from_cache_line(self, memory_addr: int) -> str:
		'''
		after knowing that the data exists, 
		return the data that is in the cache line for the processor's use. 
		
		params:
		:memory_addr (int) -  memory address of requested cache line 

		return:
		:data (str): the actual data from the cache_line

		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		1. find data for given cache line mode (this function is only called when controller doesn't already have data)
		2. return the data to the process making the request

		'''
		pass

	def get_current_cache_line_mode(self, memory_addr: int) -> int:
		'''
		gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
		if cache line entry doesn't exist: return invalid)

		params:
		:memory_addr -  memory address of requested cache line 

		return:
		:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I) as int (defined in global states)

		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		1. Ensure that address exists in memory
		2. If it exists, return the mode associated with the requested cache line information 

		'''

		print("REQUESTOR: searching cache state of memory_addr", memory_addr)

		# return mode


	def update_cache_state(self, memory_addr:int, mode:str, new_mode_value:int) -> int:
		'''
		update cache line to a new_state (generally after response from network)

		params:
		:memory_addr - address of requested block of data 
		:mode - state/mode that is being updated
		:new_mode_value - new value for given mode param

		return: boolean on successful update of cache line state

		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		1. find the cache line entry for the given memory_addr
		2. For the given mode (i.e. cache line state), must update the value to new_value (i.e. the mode may change from S --> M or I-->S)
		'''
		print("REQUESTOR: Update cache state of memory_addr", memory_addr, "with mode:", mode, "and new value:", new_mode_value)
		pass

		