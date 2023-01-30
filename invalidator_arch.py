class invalidator_arch(object):
	
	def __init__(self):
		pass

	def get_stored_cache_line_mode(self, memory_addr:int) -> int:
		'''
		gets mode (i.e. modified, shared, invalid, etc.) for a stored cache line entry; 

		if cache line entry doesn't exist: return invalid)

		params:
		:memory_addr -  memory address of requested cache line 

		return:
		:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I)


		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		Ensure that address exists in memory
		If it exists, determine the cache_line mode associated with it 
			 - ensure that address exists in cache
		'''


	def flush_cache_line_entry_to_network(self, memory_addr:int) -> int:
		'''
		params:
		:memory_addr - address of block that is being flushed

		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		Send cache line entry that is being invalidated to entry to network so that other cache controllers can access memory entry
		'''

	def update_cache_line_state(self, cache_line:int, mode:int, new_mode_value:int) -> int:
		'''
		update cache line to a new_state (generally after response from network)

		params:
		:cache_line - cache entry for page
		:mode - state/mode that is being updated
		:new_mode_value - new value for that mode/state
		
		####REQUIREMENTS FOR ARCHITECTURE DEVELOPER####
		based on a given state/mode, update the value in the cache controller for that given mode (i.e. like updating a table) 
		'''