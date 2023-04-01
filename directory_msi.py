import inspect
import textwrap
from cache_state import *
from directory import directory


class directory_msi(directory):
	def __init__(self, interconnect, directory_arch):
		super(directory_msi, self).__init__(interconnect, directory_arch)

		#valid request and response messages possible
		self.request_messages = ["getS", "getM"]
		self.response_messages = ["ACK"]

		self.match_action_table["getS"][INVALID] = [(self.respond_to_requestor_immediate, [SHARED, True])]

		self.match_action_table["getM"][INVALID] = [(self.respond_to_requestor_immediate, [MODIFIED, True])]

		self.match_action_table["getS"][SHARED] = [(self.respond_to_requestor_immediate, [SHARED, False])]

		self.match_action_table["getM"][SHARED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] #these should be directory arch functions in general

		self.match_action_table["getS"][MODIFIED] = [(self.invalidate_sharers, [SHARED, SHARED])] #these should be directory arch functions in general

		self.match_action_table["getM"][MODIFIED] = [(self.invalidate_sharers, [INVALID, MODIFIED])] #these should be directory arch functions in general, but for simulation this works

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

		requestor, new_state_requestor = "a1", MODIFIED  
		self.directory_arch.update_directory_state(args["memory_addr"], 'mode', new_state_requestor)
		self.directory_arch.update_directory_state(args["memory_addr"], 'sharers', requestor)
		self.interconnect.send_message(requestor, 'directory', ('change_state', args["memory_addr"], "mode", new_state_requestor), False)

	def run(self):
		message = self.interconnect.get_message("directory")
		args = self.parse_message(message)
		current_state = self.get_current_state(args)
		ftn_list = self.get_match_action_table_entry(args, current_state) 
		self.invoke_matched_function(ftn_list, args)

	def get_current_state(self,args):
		current_state = self.directory_arch.get_directory_state(args["memory_addr"], "mode")

		#FOR TESTING:
		current_state = SHARED
		return current_state

	def parse_message(self,message):
		args = {}
		args["dest"] = message[0]
		args["src"] = message[1]
		message_contents = message[2]
		#format of read is ("read", memory_addr)
		args["message_name"] = message_contents[0]
		if message_contents[0] == "getS" or message_contents[0] == "getM":
			args["memory_addr"] = message_contents[1]
		elif message_contents[0] == "ACK":
			args["memory_addr"] = message_contents[1]
		return args

	def get_match_action_table_entry(self, args, current_state):
		return self.match_action_table[args["message_name"]][current_state]

	def invoke_matched_function(self, ftn_list, args):
		for ftn, param in ftn_list:
			param.append(args)
			ftn(*tuple(param)) #this adds context, args to the param_list

	def update_directory_state(self, mode, new_mode_value, args):
		self.requestor_arch.update_cache_state(args["memory_addr"], mode , new_mode_value)

	def invalidate_sharers(self, new_state_invalidator, new_state_requestor, args):
		self.directory_arch.store_request(args["src"], args["memory_addr"], new_state_requestor) #store request

		sharers = self.directory_arch.get_directory_state(args["memory_addr"], "sharers")

		#FOR TESTING:
		sharers = ["a2"]
		# return current_state


		for sharer in sharers:
			self.interconnect.send_message(sharer, "directory", ("change_state", args["memory_addr"], "mode", new_state_invalidator), True)

	def get_data(self, args):
		self.directory_arch.get_data(args["memory_addr"])




