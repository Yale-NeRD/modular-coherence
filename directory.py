import inspect
import textwrap
from cache_state import *


class directory(object):
	def __init__(self,interconnect, directory_arch):

		self.directory_arch = directory_arch

		# self.cache_line_states = ["invalid", "shared", "modified"]

		self.valid_messages = ["getS", "getM", "ACK"]

		#make a table of size n x n states
		self.match_action_table = {}

		for msg in self.valid_messages:
			self.match_action_table[msg] = {}


		self.global_cache_state = {}
		#key = cache_addr
		#value = dict(data, mode, [sharers])

		self.interconnect = interconnect



