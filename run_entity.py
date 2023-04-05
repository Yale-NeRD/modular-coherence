class run_entity(object):
	def __init__(self, interconnect,invalidator_bool):
		self.interconnect = interconnect
		self.invalidator = invalidator_bool #tells interconnect whether to read from invalidator, requestor, or directory; IF true, reads from invalidator queue, if False, reads requestor queue; if None, reads directory queue (if self.name is "directory" too)

		self.match_action_table = {}
	
	def run(self, thread_return=None):
		message = self.interconnect.get_message(self.name, invalidator=self.invalidator)
		dest, src, msg_name, memory_addr, message = self.parse_message(message)
		current_state = self.get_current_state(memory_addr)
		ftn_list = self.get_match_action_table_entry(msg_name, current_state) 
		self.invoke_matched_function(ftn_list, dest, src, msg_name, memory_addr, message)

	def get_current_state(self,memory_addr):
		pass 

	def parse_message(self,message):
		dest = message[0]
		src = message[1]
		message_contents = message[2]
		msg_name = message_contents[0]
		memory_addr = message_contents[1]
		return dest, src, msg_name, memory_addr, message

	def get_match_action_table_entry(self, args, current_state):
		return self.match_action_table[args["message_name"]][current_state]

	def get_match_action_table_entry(self, msg_name, current_state):
		return self.match_action_table[msg_name][current_state]

	def invoke_matched_function(self, ftn_list, dest, src, msg_name, memory_addr, message):
		for ftn, param in ftn_list:
			new_param = param + [dest, src, msg_name, memory_addr, message]
			ftn(*tuple(new_param)) #this adds context, args to the param_list

	def debug_check_answer(self,thread_return, memory_addr):
		thread_return["success"] = self.local_cache_state[memory_addr]
		return
		

