import sys
sys.path.insert(0,"..")


import inspect
import textwrap
from cache_state_mesi import *
from invalidator.invalidator import invalidator

class invalidator_mesi(invalidator):
	def __init__(self, interconnect, invalidator_arch, local_cache_state, name="a"):
		super(invalidator_mesi, self).__init__(interconnect, invalidator_arch, name)

		self.local_cache_state = local_cache_state

		self.match_action_table["change_state"][INVALID] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][SHARED] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, []),
		                                                     (self.flush_cache_to_network, []),
															(self.send_ack_to_dir, [])]

		self.match_action_table["change_state"][EXCLUSIVE] = [(self.update_state, []),
		                                                     (self.flush_cache_to_network, []),
															(self.send_ack_to_dir, [])]


	def get_current_state(self, memory_addr):
		current_state = self.invalidator_arch.get_stored_cache_line_mode(memory_addr)

		#FOR TESTING:
		current_state = INVALID
		if memory_addr in self.local_cache_state:
			current_state = self.local_cache_state[memory_addr]
		return current_state

	def flush_cache_to_network(self, dest, src, msg_name, memory_addr, message):
		self.invalidator_arch.flush_cache_line_entry_to_network(memory_addr)

	def send_ack_to_dir(self,  dest, src, msg_name, memory_addr, message):
		self.interconnect.send_message('directory', self.name, ("ACK", memory_addr))

	def update_state(self, dest, src, msg_name, memory_addr, message):
		mode = message[2][2]
		new_mode_value = message[2][3]
		self.invalidator_arch.update_cache_state(memory_addr, mode, new_mode_value)

