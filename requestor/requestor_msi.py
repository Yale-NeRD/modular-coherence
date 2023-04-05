import sys
sys.path.insert(0,"..")

import inspect
import textwrap
from requestor.requestor import requestor
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


	def get_current_state(self,args):
		current_state = self.requestor_arch.get_current_cache_line_mode(args["memory_addr"])
		#FOR TESTING:
		current_state = INVALID
		return current_state

	def send_invalidation_to_dir(self, message, args,f=None):
		self.interconnect.send_message('directory', self.name, (message, args["memory_addr"]))
		print("SEND_MESSAGE TO DIRECTORY")
		# if f is not None:
		# 	f.write(f"interconnect__send_message('directory', self_name, ({message}, args['memory_addr']))")

	def update_state(self, args, f=None):
		self.requestor_arch.update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
		# if f is not none:
		# 	f.write(f"requestor_arch__update_cache_state(args['memory_addr'], args['mode'], args['new_mode_value'])")
