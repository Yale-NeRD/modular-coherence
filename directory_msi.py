import inspect
import textwrap
from cache_state import *
from directory import directory


class directory_msi(directory):
	def __init__(self):
		super(directory_msi, self).__init__()


		self.match_action_table[INVALID]["read"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table[INVALID]["write"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


		self.match_action_table[SHARED]["read"] = ["get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"] 
		self.match_action_table[SHARED]["write"] = ["self.invalidate_sharers(memory_addr, new_mode='invalid')","get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]

		self.match_action_table[MODIFIED]["read"] = ["self.invalidate_sharers(memory_addr, new_mode='shared')", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table[MODIFIED]["write"] = ["self.invalidate_sharers(memory_addr, new_mode='invalid')", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


	def collect_and_respond_requests(self, memory_addr:int, requested_mode:int) -> int:
		'''

		params:
		:memory_addr - address of requested block
		:requested_mode - new permissions mode for the requested block

		return:
		NONE
		'''

		cache_state = self.global_cache_state[memory_addr]["mode"]
		for item in self.match_action_table[cache_state][requested_mode]:
			print("directory_" + item)
			if "self.invalidate_sharers" in item:
				eval(item)


	def invalidate_sharers(self, memory_addr, new_mode):
		for sharer in self.global_cache_state[memory_addr]["sharers"]:
			print("directory_invalidating_sharer_" + sharer.invalidator.name)
			sharer.invalidator.invalidate_cache_line_entry(memory_addr, new_mode)




