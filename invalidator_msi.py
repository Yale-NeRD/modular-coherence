import inspect
import textwrap
# from invalidator_arch import invalidator_arch
from cache_state import *
from invalidator import invalidator

class invalidator_msi(invalidator):
	def __init__(self, interconnect, invalidator_arch, local_cache_state, name="a"):
		super(invalidator_msi, self).__init__(interconnect, invalidator_arch, name)

		self.local_cache_state = local_cache_state

		self.match_action_table["change_state"][INVALID] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][SHARED] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, []),
		                                                     (self.flush_cache_to_network, []),
															(self.send_ack_to_dir, [])]

	def run(self):
		message = self.interconnect.get_message(self.name, invalidator=True)
		args = self.parse_message(message)
		current_state = self.get_current_state(args)
		ftn_list = self.get_match_action_table_entry(args, current_state) 
		self.invoke_matched_function(ftn_list, args)

	def get_current_state(self, args):
		current_state = self.invalidator_arch.get_stored_cache_line_mode(args["memory_addr"])

		#FOR TESTING:
		current_state = MODIFIED
		return current_state

	def parse_message(self, message):
		args = {}
		args["dest"] = message[0]
		args["src"] = message[1]
		message_contents = message[2]
		args["message_name"] = message_contents[0]
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
			param.append(args)
			ftn(*tuple(param)) #this adds context, args to the param_list

	def flush_cache_to_network(self, args):
		self.invalidator_arch.flush_cache_line_entry_to_network(args["memory_addr"])

	def send_ack_to_dir(self, args):
		self.interconnect.send_message('directory', self.name, ("ACK", args["memory_addr"]))

	def update_state(self, args):
		self.invalidator_arch.update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])

