import inspect
import textwrap

###STATE DEFINITIONS###
MODIFIED = 2
SHARED = 1
INVALID = 0


class invalidator():
	def __init__(self):
		cache_entry_states = {
			"modified":2,
			"shared":1,
			"invalid":0
			}


	def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		TODO
		'''
		if data_required:
			self.flush_page_to_network(memory_addr)
		if remove_data == True:
			self.update_cache_state(cache_line, "mode", 0)
		if remove_data == False:
			self.update_cache_state(cache_line, "mode", 1)


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



###DO NOT CHANGE BELOW THIS