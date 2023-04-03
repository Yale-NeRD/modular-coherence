class run_entity(object):
	def __init__(self, interconnect,invalidator_bool):
		self.interconnect = interconnect
		self.invalidator = invalidator_bool #tells interconnect whether to read from invalidator, requestor, or directory; IF true, reads from invalidator queue, if False, reads requestor queue; if None, reads directory queue (if self.name is "directory" too)

		self.match_action_table = {}
	
	def run(self):
		message = self.interconnect.get_message(self.name, invalidator=self.invalidator)
		args = self.parse_message(message)
		current_state = self.get_current_state(args)
		ftn_list = self.get_match_action_table_entry(args, current_state) 
		self.invoke_matched_function(ftn_list, args)

	def get_current_state(self,args):
		pass 

	def parse_message(self,message):
		args = {}
		args["dest"] = message[0]
		args["src"] = message[1]
		message_contents = message[2]
		#format of read is ("read", memory_addr)

		args["message_name"] = message_contents[0]

		#this is request to requestor 
		if message_contents[0] == "read" or message_contents[0] == "write":
			args["memory_addr"] = message_contents[1]
		#format of change_state is ("change_state", mode, MODIFIED); ONLY SEEN BY REQUESTOR/INVALIDATOR
		elif message_contents[0] == "change_state":
			args["memory_addr"] = message_contents[1]
			args["mode"] = message_contents[2]
			args["new_mode_value"] = message_contents[3]

		#BELOW TWO ARE ONLY FOR DIRECTORY
		elif message_contents[0] == "getS" or message_contents[0] == "getM":
			args["memory_addr"] = message_contents[1]
		elif message_contents[0] == "ACK":
			args["memory_addr"] = message_contents[1]
		else:
			print("ERROR") #TODO, CHANGE TO RAISE ERROR 
		return args

	def get_match_action_table_entry(self, args, current_state):
		return self.match_action_table[args["message_name"]][current_state]

	def invoke_matched_function(self, ftn_list, args, f=None):
		for ftn, param in ftn_list:
			param.append(args)
			ftn(*tuple(param)) #this adds context, args to the param_list