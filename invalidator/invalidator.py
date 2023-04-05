import sys
sys.path.insert(0,"..")


import inspect
import textwrap
# from invalidator_arch import invalidator_arch
from cache_state import *
from run_entity import run_entity

class invalidator(run_entity):
	def __init__(self, interconnect, invalidator_arch, name="a"):
		super(invalidator, self).__init__(interconnect, True)

		self.name = name

		self.invalidator_arch = invalidator_arch
		
		self.valid_messages = ["change_state"]


		self.match_action_table = {}

		for msg in self.valid_messages:
			self.match_action_table[msg] = {}

		self.interconnect = interconnect




