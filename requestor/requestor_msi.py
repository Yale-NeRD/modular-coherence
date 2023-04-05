import sys
sys.path.insert(0,"..")

import inspect
import textwrap
from requestor.requestor import requestor
from cache_state import *

class requestor_msi(requestor):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, interconnect, requestor_arch, directory, local_cache_state, name):
		super(requestor_msi, self).__init__(interconnect, requestor_arch, directory, name)

		self.local_cache_state = local_cache_state

		self.match_action_table["read"][MODIFIED] = []
		self.match_action_table["write"][MODIFIED] = []

		self.match_action_table["read"] [SHARED]= []
		self.match_action_table["write"][SHARED] = [(self.send_invalidation_to_dir, ['getM'])]

		self.match_action_table["read"][INVALID] = [(self.send_invalidation_to_dir, ['getS'])]
		self.match_action_table["write"][INVALID]= [(self.send_invalidation_to_dir, ['getM'])]


		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, [])]
		self.match_action_table["change_state"][INVALID] = [(self.update_state, [])]
		self.match_action_table["change_state"][SHARED] = [(self.update_state, [])]

	def get_current_state(self,memory_addr):
		current_state = self.requestor_arch.get_current_cache_line_mode(memory_addr)


		#FOR TESTING:
		current_state = INVALID
		if memory_addr in self.local_cache_state:
			current_state = self.local_cache_state[memory_addr]
		return current_state

	def send_invalidation_to_dir(self, message_new, dest, src, msg_name, memory_addr, message):
		self.interconnect.send_message('directory', self.name, (message_new, memory_addr))
		print("SEND_MESSAGE TO DIRECTORY")
	
	def update_state(self, args, f=None):
		self.requestor_arch.update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
	
	def update_state(self, dest, src, msg_name, memory_addr, message):
		mode = message[2][2]
		new_mode_value = message[2][3]
		self.requestor_arch.update_cache_state(memory_addr, mode, new_mode_value)

		#FOR TESTING
		self.local_cache_state[memory_addr] = new_mode_value
		
