import inspect
import textwrap
from cache_state import *
from directory import directory


class directory_msi(directory):
	def __init__(self, directory_arch):
		super(directory_msi, self).__init__(directory_arch)


		self.match_action_table[INVALID]["getS"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table[INVALID]["getM"] = ["fetch_data_ext(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


		self.match_action_table[SHARED]["getS"] = ["get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"] 
		self.match_action_table[SHARED]["getM"] = ["self.directory_arch.invalidate_sharers(sharers, memory_addr, new_mode=INVALID)","get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]

		self.match_action_table[MODIFIED]["getS"] = ["self.directory_arch.invalidate_sharers(sharers, memory_addr, new_mode=SHARED)", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, shared)", "update_state()"]
		self.match_action_table[MODIFIED]["getM"] = ["self.directory_arch.invalidate_sharers(sharers, memory_addr, new_mode=INVALID)", "get_data(memory_addr)", "respond_to_requestor(memory_addr, data, modified)", "update_state()"]


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
			if "directory_arch.invalidate_sharers" in item:
				sharers = self.global_cache_state[memory_addr]["sharers"]
				eval(item)
			else:
				print("directory_" + item)


	# def invalidate_sharers(self, memory_addr, new_mode):





