import inspect
import textwrap
from requestor_arch import requestor_arch
from requestor import requestor
from cache_state import *


class requestor_msi(requestor):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, interconnect, requestor_arch, directory, local_cache_state, name):
		super(requestor_msi, self).__init__(interconnect, requestor_arch, directory, name)

		self.local_cache_state = local_cache_state

		# self.match_action_table[SHARED]["write"] = ['directory', self.name, 'getM', memory_addr]

		self.match_action_table["read"][MODIFIED] = []
		self.match_action_table["write"][MODIFIED] = []

		self.match_action_table["read"] [SHARED]= []
		self.match_action_table["write"][SHARED] = [(self.send_invalidation_to_dir, ['getM'])]

		self.match_action_table["read"][INVALID] = [(self.send_invalidation_to_dir, ['getS'])]
		self.match_action_table["write"][INVALID]= [(self.send_invalidation_to_dir, ['getM'])]


		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, [])]
		self.match_action_table["change_state"][INVALID] = [(self.update_state, [])]
		self.match_action_table["change_state"][SHARED] = [(self.update_state, [])]

	def run(self):
		f = open("test.c", "a")
		message = self.interconnect.get_message(self.name, invalidator=False)
		args = self.parse_message(message)
		current_state = self.get_current_state(args)
		ftn_list = self.get_match_action_table_entry(args, current_state) 
		self.invoke_matched_function(ftn_list, args, f)

	def get_current_state(self,args):
		current_state = self.requestor_arch.get_current_cache_line_mode(args["memory_addr"])
		#FOR TESTING:
		current_state = INVALID
		return current_state

	def parse_message(self,message):
		args = {}
		args["dest"] = message[0]
		args["src"] = message[1]
		message_contents = message[2]
		#format of read is ("read", memory_addr)

		args["message_name"] = message_contents[0]
		if message_contents[0] == "read" or message_contents[0] == "write":
			args["memory_addr"] = message_contents[1]
		#format of change_state is ("change_state", mode, MODIFIED)
		elif message_contents[0] == "change_state":
			args["memory_addr"] = message_contents[1]
			args["mode"] = message_contents[2]
			args["new_mode_value"] = message_contents[3]
		else:
			print("ERROR") #TODO, CHANGE TO RAISE ERROR 
		return args

	def get_match_action_table_entry(self, args, current_state):
		return self.match_action_table[args["message_name"]][current_state]

	def invoke_matched_function(self, ftn_list, args, f):
		for ftn, param in ftn_list:
			param.append(args)
			param.append(f)
			ftn(*tuple(param)) #this adds context, args to the param_list

	def send_invalidation_to_dir(self, message, args, f):
		self.interconnect.send_message('directory', self.name, (message, args["memory_addr"]))
		f.write("TESTING123")

	def update_state(self, args, f):
		self.requestor_arch.update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
		f.write("456TESTING456")
