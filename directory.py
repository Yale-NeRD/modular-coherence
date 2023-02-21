import inspect
import textwrap

###STATE DEFINITIONS###
MODIFIED = 2
SHARED = 1
INVALID = 0

class directory(object):
	def __init__(self):

		self.number_of_states = 3 #n
		self.cache_line_states = ["invalid", "shared", "modified"]

		#make a table of size n x n states
		self.match_action_table = {}

		self.global_cache_state = {}
		#key = cache_addr
		#value = dict(data, mode, [sharers])

	def collect_and_respond_requests(self, memory_addr:int, requested_mode:int) -> int:
		'''

		params:
		:memory_addr - address of requested block
		:requested_mode - new permissions mode for the requested block

		return:
		NONE
		'''


		for state in self.cache_line_states:
			self.match_action_table[state] = {}
			for matched_state in self.cache_line_states:
				self.match_action_table[state][matched_state] = None
		

		# first value in match action table = global state (what directory knows about the memory_addr)
		# second value in match action tabel is the incoming request (which is always either read, write), since shim layer should deny any other request
		self.match_action_table["invalid"]["read"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table["invalid"]["write"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


		self.match_action_table["shared"]["read"] = ["get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"] 
		self.match_action_table["shared"]["write"] = ["self.invalidate_sharers(memory_addr, new_mode='invalid')","get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]

		self.match_action_table["modified"]["read"] = ["self.invalidate_sharers(memory_addr, new_mode='shared')", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table["modified"]["write"] = ["self.invalidate_sharers(memory_addr, new_mode='invalid')", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


		cache_state = self.global_cache_state[memory_addr]["mode"]
		for item in self.match_action_table[cache_state][requested_mode]:
			print("directory_" + item)
			if "self.invalidate_sharers" in item:
				eval(item)


	def invalidate_sharers(self, memory_addr, new_mode):
		for sharer in self.global_cache_state[memory_addr]["sharers"]:
			print("directory_invalidating_sharer_" + sharer.name)
			sharer.invalidate_cache_line_entry(memory_addr, new_mode)




