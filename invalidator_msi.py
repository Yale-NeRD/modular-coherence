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

		self.match_action_table["change_state"][INVALID] = [(self.update_state, ()),
															(self.send_ack_to_dir, ())] 

		self.match_action_table["change_state"][SHARED] = [(self.update_state, ()),
															(self.send_ack_to_dir, ())] 

		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, ()),
		                                                     (self.flush_cache_to_network, ()),
															(self.send_ack_to_dir, ())]

		while True:
			request = self.interconnect.get_queue_element(self.name, invalidator=True)
			if request is not None:
				message_name, arguments, sender = request

				if message_name == "change_state":
					new_state, memory_addr = arguments
					self.invalidator_arch.update_cache_line_state(memory_addr, "mode", new_state) #use architecture to update state
					self.local_cache_state[memory_addr] = new_state #can be removed 

					if self.local_cache_state[memory_addr] == MODIFIED:
						self.invalidator_arch.flush_cache_line_entry_to_network(memory_addr)


					self.interconnect.send_message("directory", self.name, "ACK", memory_addr) #send ack once invalidation has occured
					return
		return 

	def parse_message(message):
		args = {}
		args["dest"] = message[0]
		args["src"] = message[1]
		message_contents = message[2]
		if message_contents[0] == "change_state":
			args["memory_addr"] = message_contents[1]
			args["mode"] = message_contents[2]
			args["new_mode_value"] = message_contents[3]
		else:
			print("ERROR") #TODO, CHANGE TO RAISE ERROR 
		return args

	def get_match_action_table_entry(self, args, current_state):
		return self.match_action_table[args["message_name"]][current_state]

	def invoke_matched_function(self, ftn_list, args):
		for ftn, param in ftn_list:
			new_param = param + (args) #this adds context, args to the param_list
			ftn(*new_param)

	def flush_cache_to_network(self, args):
		self.invalidator_arch.flush_cache_line_entry_to_network(args["memory_addr"])

	def send_ack_to_dir(self, args):
		self.interconnect.send_message('directory', self.name, ("ACK", args["memory_addr"]))

	def update_state(self, args):
		self.invalidator_arch.update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"] 

