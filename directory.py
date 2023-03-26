import inspect
import textwrap
from cache_state import *


class directory(object):
	def __init__(self,interconnect, directory_arch):

		self.directory_arch = directory_arch

		self.cache_line_states = ["invalid", "shared", "modified"]

		#make a table of size n x n states
		self.match_action_table_requests = {}
		self.match_action_table_responses = {}

		for state in cache_line_states:
			self.match_action_table_requests[state] = {}
			self.match_action_table_responses[state] = {}


		self.global_cache_state = {}
		#key = cache_addr
		#value = dict(data, mode, [sharers])

		self.interconnect = interconnect



