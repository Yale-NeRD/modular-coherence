class invalidator_arch(object):
	
	def __init__(self):
		pass

	def get_stored_cache_line_mode(self, memory_addr:int) -> int:
		'''
		gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
		if cache line entry doesn't exist: return invalid)

		params:
		:memory_addr -  memory address of requested cache line 

		return:
		:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I)

		'''
		# return mode

		'''
		expected semantics for architecture developer:
			 - ensure that address exists in cache
		'''

	# def invalidate_cache(address):
	# 	'''
	# 	invalidates a page (makes state I)

	# 	params:
	# 	: address - page being invalidated
	# 	'''

	# 	'''for developer:
	# 	- invalidate the page entry and flush the page to local HW (and also other parts of the same cache region)
	# 	- up to mind developer if they want to do this async or sync 
		# '''



	def flush_cache_line_entry_to_network(self, memory_addr:int) -> int:
		'''
		params:
		:memory_addr - address of block that is being flushed
		'''


		'''for MIND developer:
		- send the entire page to the rest of the network (i.e. to the requestor thats asking for a page)
		'''

	def update_cache_line_state(self, cache_line:int, state:int, new_value:int) -> int:
		'''
		update cache line to a new_state (generally after response from network)

		params:
		:cache_line - cache entry for page
		:state - state that is being updated
		:new_value - new value for state
		'''

		'''
		expected semantics for MIND developer:
			 -  the states that are encoded should match what's the bits of information that are in PTE
			 - needs to simply update cache
		'''