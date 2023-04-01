import inspect
import textwrap
# from invalidator_arch import invalidator_arch
from cache_state import *

class invalidator(object):
	def __init__(self, interconnect, invalidator_arch, name="a"):
		self.name = name

		self.invalidator_arch = invalidator_arch

		self.match_action_table = {}

		self.valid_messages = ["change_state"]

		for msg in self.valid_messages:
			self.match_action_table[msg] = {}

		self.interconnect = interconnect
		self.invalidator_queue = self.interconnect.controller_queues[self.name]["invalidator"]


		#key = memory_addr
		#value = cache state/mode

	# def invalidate_cache_line_entry(self, memory_addr:int, new_mode:int) -> int:
	# 	'''
	# 	given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

	# 	params:
	# 	:address - address of requested block
	# 	:new_mode - new permissions mode for the requested block

	# 	return:
	# 	NONE
	# 	'''


	# 	pass

