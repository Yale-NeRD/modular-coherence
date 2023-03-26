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


	def get_cache_line_entry(self, memory_addr:int, requested_mode:str) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in (TODO: should be read, write)

		return:
		:data (str): the actual data from the cache line after it has been received
		'''

		self.match_action_table[MODIFIED]["read"] = []
		self.match_action_table[MODIFIED]["write"] = []

		self.match_action_table[SHARED]["read"] = []
		self.match_action_table[SHARED]["write"] = ['directory', self.name, 'getM', memory_addr]

		self.match_action_table[INVALID]["read"] = ['directory', self.name, 'getS', memory_addr]
		self.match_action_table[INVALID]["write"] = ['directory', self.name, 'getM', memory_addr]



		cache_state = INVALID
		if memory_addr in self.local_cache_state:
			cache_state = self.local_cache_state[memory_addr] #should be implemented via the architecture code 
		# for func, param in self.match_action_table[cache_state][requested_mode]:
		action_table_entry = self.match_action_table[cache_state][requested_mode]

		if len(action_table_entry) == 0:
			#this is when the list of match action table is less than 0. In this case, don't do anything for now
			#TODO, figure out if I need to return anything here (i.e. the actual data)
			pass
		else:
			#otherwise send message
			self.interconnect.send_message(action_table_entry[0], action_table_entry[1], action_table_entry[2], action_table_entry[3])

	def read_queue(self, thread_return):
		while True:
			request = self.interconnect.get_queue_element(self.name, invalidator=False)
			if request is not None:
				message_name, arguments, sender = request
				if message_name == "change_state":
					state, address = arguments
					self.local_cache_state[address] = state
				print("request read by requestor", request, self.local_cache_state[address])
				thread_return["success"] = self.local_cache_state[address]
				return






