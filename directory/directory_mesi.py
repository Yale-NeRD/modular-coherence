import sys
sys.path.insert(0,"..")

import inspect
import textwrap
from cache_state_mesi import *
from directory.directory import directory


class directory_mesi(directory):
	def __init__(self, interconnect, directory_arch, directory_cache_state):
		super(directory_mesi, self).__init__(interconnect, directory_arch)

		self.requests = {}

		self.directory_cache_state = directory_cache_state

		self.match_action_table["getS"][INVALID] = [(self.respond_to_requestor_immediate, [EXCLUSIVE, True])]

		self.match_action_table["getM"][INVALID] = [(self.respond_to_requestor_immediate, [MODIFIED, True])]

		self.match_action_table["getS"][SHARED] = [(self.respond_to_requestor_immediate, [SHARED, False])]

		self.match_action_table["getM"][SHARED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] 

		self.match_action_table["getS"][MODIFIED] = [(self.invalidate_sharers, [INVALID, EXCLUSIVE])] 

		self.match_action_table["getM"][MODIFIED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] 

		self.match_action_table["getS"][EXCLUSIVE] = [(self.invalidate_sharers, [SHARED, SHARED])] 

		self.match_action_table["getM"][EXCLUSIVE] = [(self.invalidate_sharers, [INVALID, MODIFIED])] #NEW STATE IS EXCLUSIVE
		

		self.match_action_table["ACK"][INVALID] = []
		self.match_action_table["ACK"][SHARED] = [(self.respond_to_requestor_after_invalidator, [])]
		self.match_action_table["ACK"][MODIFIED] = [(self.respond_to_requestor_after_invalidator, [])]

	def respond_to_requestor_immediate(self, new_state, update_directory_internal_state, dest, src, msg_name, memory_addr, message):
		data = self.directory_arch.get_data(memory_addr)
		if update_directory_internal_state:
			self.directory_arch.update_directory_state(memory_addr, 'mode', new_state)
		self.directory_arch.update_directory_state(memory_addr, 'sharers', src)
		self.interconnect.send_message(src, 'directory', ('change_state', memory_addr, "mode", new_state), False)

	def respond_to_requestor_after_invalidator(self, dest, src, msg_name, memory_addr, message):
		requestor, new_state_requestor = self.directory_arch.get_request(memory_addr) #get request

		requestor, new_state_requestor = self.requests[memory_addr]  #FOR SAKE OF TESITNG, CAN BE REMOVED IN FUTURE

		self.directory_arch.update_directory_state(memory_addr, 'mode', new_state_requestor)
		self.directory_arch.update_directory_state(memory_addr, 'sharers', requestor)
		self.interconnect.send_message(requestor, 'directory', ('change_state', memory_addr, "mode", new_state_requestor), False)

	def get_current_state(self,memory_addr):
		#FOR TESTING:
		current_state = INVALID
		if memory_addr in self.directory_cache_state:
			current_state = self.directory_cache_state[memory_addr]["mode"]
		return current_state


	def invalidate_sharers(self, new_state_invalidator, new_state_requestor, dest, src, msg_name, memory_addr, message):
		self.directory_arch.store_request(src, memory_addr, new_state_requestor) #store request
		sharers = self.directory_arch.get_directory_state(memory_addr, "sharers")

		#FOR TESTING:
		self.requests[memory_addr] = (src, new_state_requestor)
		sharers = self.directory_cache_state[memory_addr]["sharers"]
		for sharer in sharers:
			self.interconnect.send_message(sharer, "directory", ("change_state", memory_addr, "mode", new_state_invalidator), True)


	def get_data(self, dest, src, msg_name, memory_addr, message):
		self.directory_arch.get_data(memory_addr)




