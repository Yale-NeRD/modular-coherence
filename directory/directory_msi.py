import sys
sys.path.insert(0,"..")

import inspect
import textwrap
from cache_state import *
from directory.directory import directory


class directory_msi(directory):
	def __init__(self, interconnect, directory_arch):
		super(directory_msi, self).__init__(interconnect, directory_arch)

		#valid request and response messages possible

		self.match_action_table["getS"][INVALID] = [(self.respond_to_requestor_immediate, [SHARED, True])]

		self.match_action_table["getM"][INVALID] = [(self.respond_to_requestor_immediate, [MODIFIED, True])]

		self.match_action_table["getS"][SHARED] = [(self.respond_to_requestor_immediate, [SHARED, False])]

		self.match_action_table["getM"][SHARED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] #these should be directory arch functions in general

		self.match_action_table["getS"][MODIFIED] = [(self.invalidate_sharers, [SHARED, SHARED])] #these should be directory arch functions in general

		self.match_action_table["getM"][MODIFIED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] #these should be directory arch functions in general, but for simulation this works

		self.match_action_table["ACK"][INVALID] = []
		self.match_action_table["ACK"][SHARED] = [(self.respond_to_requestor_after_invalidator, [])]
		self.match_action_table["ACK"][MODIFIED] = [(self.respond_to_requestor_after_invalidator, [])]

	def respond_to_requestor_immediate(self, new_state, update_directory_internal_state, args):
		data = self.directory_arch.get_data(args["memory_addr"])
		if update_directory_internal_state:
			self.directory_arch.update_directory_state(args["memory_addr"], 'mode', new_state)
		self.directory_arch.update_directory_state(args["memory_addr"], 'sharers', args['src'])
		self.interconnect.send_message(args['src'], 'directory', ('change_state', args["memory_addr"], "mode", new_state), False)

	def respond_to_requestor_after_invalidator(self, args):
		requestor, new_state_requestor = self.directory_arch.get_request(args["memory_addr"]) #get request
		requestor, new_state_requestor = "a1", MODIFIED  #FOR SAKE OF TESITNG, CAN BE REMOVED IN FUTURE
		self.directory_arch.update_directory_state(args["memory_addr"], 'mode', new_state_requestor)
		self.directory_arch.update_directory_state(args["memory_addr"], 'sharers', requestor)
		self.interconnect.send_message(requestor, 'directory', ('change_state', args["memory_addr"], "mode", new_state_requestor), False)

	def get_current_state(self,args):
		current_state = self.directory_arch.get_directory_state(args["memory_addr"], "mode")

		#FOR TESTING:
		current_state = SHARED
		return current_state

	def update_directory_state(self, mode, new_mode_value, args):
		self.requestor_arch.update_cache_state(args["memory_addr"], mode , new_mode_value)

	def invalidate_sharers(self, new_state_invalidator, new_state_requestor, args):
		self.directory_arch.store_request(args["src"], args["memory_addr"], new_state_requestor) #store request
		sharers = self.directory_arch.get_directory_state(args["memory_addr"], "sharers")

		#FOR TESTING:
		sharers = ["a2"]
		for sharer in sharers:
			self.interconnect.send_message(sharer, "directory", ("change_state", args["memory_addr"], "mode", new_state_invalidator), True)

	def get_data(self, args):
		self.directory_arch.get_data(args["memory_addr"])




