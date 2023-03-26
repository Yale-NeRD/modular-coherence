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


		#match action table for requetots from requestors 

		self.match_action_table_requests[INVALID]["getS"] = ["self.directory_arch.get_data(memory_addr)", 
															 "self.directory_arch.update_directory_state(memory_addr, 'mode', SHARED)", 
													 		 "self.directory_arch.update_directory_state(memory_addr, 'sharers', sender)",
													 		 "self.interconnect.send_message(sender, 'directory', 'change_state', (SHARED, memory_addr), invalidator=False)"
													 		]

		self.match_action_table_requests[INVALID]["getM"] = ["self.directory_arch.get_data(memory_addr)", 
															 "self.directory_arch.update_directory_state(memory_addr, 'mode', MODIFIED)", 
													 		 "self.directory_arch.update_directory_state(memory_addr, 'sharers', sender)",
													 		 "self.interconnect.send_message(sender, 'directory', 'change_state', (MODIFIED, memory_addr), invalidator=False)"
													 		]

		self.match_action_table_requests[SHARED]["getS"] = ["self.directory_arch.get_data(memory_addr)",
															"self.directory_arch.update_directory_state(memory_addr, 'sharers', sender)" 
															"self.interconnect.send_message(sender, 'directory', 'change_state', (SHARED, memory_addr), invalidator=False)"
															] 
		self.match_action_table_requests[SHARED]["getM"] = ["self.invalidate_sharers(memory_addr, INVALID)"]
		self.match_action_table_requests[MODIFIED]["getS"] = ["self.invalidate_sharers(memory_addr, SHARED)"]
		self.match_action_table_requests[MODIFIED]["getM"] = ["self.invalidate_sharers(memory_addr, INVALID)"]


		#responses from invalidators (only two separate actions can be made )
		self.match_action_table_responses[SHARED] = ["self.directory_arch.update_directory_state(memory_addr, 'mode', SHARED)", 
													 "self.directory_arch.update_directory_state(memory_addr, 'sharers', sender)", 
													 "self.directory_arch.get_data(memory_addr)"]
		self.match_action_table_responses[MODIFIED] = ["self.directory_arch.update_directory_state(memory_addr, 'mode', MODIFIED)", 
											 		   "self.directory_arch.update_directory_state(memory_addr, 'sharers', sender)", 
											           "self.directory_arch.get_data(memory_addr)"]

		#store all requests made 							        
		self.requests_made = {}


	def collect_and_respond_requests(self):
		while True:
			if len(self.interconnect.directory_queue) != 0:
				message_name, arguments, sender = self.interconnect.directory_queue.pop()
				if message_name in self.request_messages:
					memory_addr = arguments
					cache_state = self.global_cache_state[memory_addr]["mode"]
					self.requests_made[memory_addr] = (sender, message_name)
					for item in self.match_action_table_requests[cache_state][message_name]:
						eval(item)
				
				elif message_name in self.response_messages and message_name == "ACK":
					print("ACK received by directory by", sender)
					memory_addr = arguments
					sender, new_mode = self.requests_made[memory_addr]
					if new_mode == "getM":
						new_mode = MODIFIED
					elif new_mode == "getS":
						new_mode = SHARED

					for func in self.match_action_table_responses[new_mode]:
						eval(func)
					self.interconnect.send_message(sender, "directory", "change_state", (new_mode, memory_addr), invalidator=False)


	def invalidate_sharers(self, memory_addr, new_mode):
		sharers = self.global_cache_state[memory_addr]["sharers"]
		for sharer in sharers:
			self.interconnect.send_message(sharer, "directory", "change_state", (new_mode, memory_addr), invalidator=True)





