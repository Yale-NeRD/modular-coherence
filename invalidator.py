class Invalidator():
	def __init__(self):
		cache_entry_states = 
			{
			"modified":2,
			"shared":1,
			"invalid":0
			}


	def invalidate_cache_line_entry(self, memory_addr, new_mode):
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		TODO
		'''


	def get_stored_cache_line_mode(self, memory_addr):
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

	# def invalidate_page(address):
	# 	'''
	# 	invalidates a page (makes state I)

	# 	params:
	# 	: address - page being invalidated
	# 	'''

	# 	'''for developer:
	# 	- invalidate the page entry and flush the page to local HW (and also other parts of the same cache region)
	# 	- up to mind developer if they want to do this async or sync 
	# 	'''



	def flush_cache_line_entry_to_network(self, memory_addr):
		'''
		params:
		:memory_addr - address of block that is being flushed
		'''


		'''for MIND developer:
		- send the entire page to the rest of the network (i.e. to the requestor thats asking for a page)
		'''

	def update_cache_line_state(cache_line, state, new_value):
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





	##example implementation of invalidation
	def do_disagg_invalidation(address, remove_data, data_required):
		'''
		main function called upon a invalidation request

		params:
		:address - vma of page being invalidated
		:remove_data - boolean on whether page is being invalidated (new state is I)
		:data_required - boolean on whether data must be flushed to network
		^^current assumption is that these are provided by the directory (very possible to change this)
		
		'''
		if data_required:
			flush_page_to_network(address)
		if remove_data:
			update_cache_state(cache_line, "present_bit", 0)
			invalidate_page(address)
		else:
			update_cache_state(cache_line, "write_bit", 1)









