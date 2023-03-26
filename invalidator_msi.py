import inspect
import textwrap
# from invalidator_arch import invalidator_arch
from cache_state import *
from invalidator import invalidator

class invalidator_msi(invalidator):
	def __init__(self, interconnect, invalidator_arch, local_cache_state, name="a"):
		super(invalidator_msi, self).__init__(interconnect, invalidator_arch, name)

		self.local_cache_state = local_cache_state



	def invalidate_cache_line_entry(self) -> int:
		'''
		given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

		params:
		:address - address of requested block
		:new_mode - new permissions mode for the requested block

		return:
		NONE
		'''

		# # self.match_action_table[SHARED][INVALID] = ["invalidator_arch.update_cache_line_state(self,memory_addr, 'mode', INVALID)"] 
		# # self.match_action_table[SHARED][SHARED] = [] 
		# # self.match_action_table[SHARED][MODIFIED] = []

		# # self.match_action_table[MODIFIED][INVALID] = ["invalidator_arch.flush_cache_line_entry_to_network(self,memory_addr)", 
		# # 												 "invalidator_arch.update_cache_line_state(self, memory_addr, 'mode', INVALID)"]
		# # self.match_action_table[MODIFIED][SHARED] = ["invalidator_arch.flush_cache_line_entry_to_network(self,memory_addr)", 
		# # 												 "invalidator_arch.update_cache_line_state(self,memory_addr, 'mode', SHARED)"]
		# # self.match_action_table[MODIFIED][MODIFIED] = []
		# self.match_action_table[MODIFIED][INVALID] = ["self.flush_cache_line_entry_to_network(memory_addr)"]

		while True:
			request = self.interconnect.get_queue_element(self.name, invalidator=True)
			if request is not None:
				message_name, arguments, sender = request

				if message_name == "change_state":
					new_state, memory_addr = arguments
					self.invalidator_arch.update_cache_line_state(memory_addr, "mode", new_state) #use architecture to update state
					self.local_cache_state[memory_addr] = new_state

					if self.local_cache_state[memory_addr] == MODIFIED:
						self.invalidator_arch.flush_cache_line_entry_to_network(memory_addr)


					self.interconnect.send_message("directory", self.name, "ACK", memory_addr) #send ack once invalidation has occured
					return
		return 

