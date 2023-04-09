import sys
sys.path.insert(0,"..")

import inspect
import textwrap
from requestor.requestor import requestor
from cache_state_mosi import *

class requestor_mosi(requestor):
	#cache entry states must be defined by cache coherence developer 
	def __init__(self, interconnect, requestor_arch, directory, local_cache_state, name):
		super(requestor_mosi, self).__init__(interconnect, requestor_arch, directory, name)

		self.local_cache_state = local_cache_state

		self.match_action_table["read"][] = []
		self.match_action_table["write"][MODIFIED] = []

		self.match_action_table["read"] [SHARED]= []
		self.match_action_table["write"][SHARED] = [(self.send_invalidation_to_dir, ['getM'])]

		self.match_action_table["read"][INVALID] = [(self.send_invalidation_to_dir, ['getS'])]
		self.match_action_table["write"][INVALID]= [(self.send_invalidation_to_dir, ['getM'])]

		self.match_action_table["read"][OWNED] = []
		self.match_action_table["write"][OWNED]= [(self.send_invalidation_to_dir, ['getM'])]


		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, [])]
		self.match_action_table["change_state"][INVALID] = [(self.update_state, [])]
		self.match_action_table["change_state"][SHARED] = [(self.update_state, [])]

	def get_current_state(self,memory_addr):
		"""
	    gets current state of cache block for memory_addr in requestor entity 

	    Parameters
	    ----------
	    memory_addr : int - address of block being requested 

	    Returns
	    -------
	    int
	        current mode of cache block in requestor entity

		"""
		current_state = self.requestor_arch.get_current_cache_line_mode(memory_addr)

		#FOR TESTING:
		current_state = INVALID
		if memory_addr in self.local_cache_state:
			current_state = self.local_cache_state[memory_addr]
		return current_state

	def send_invalidation_to_dir(self, message_new, dest, src, msg_name, memory_addr, message):
		"""
	    sends an invalidation request to directory from requestor 

	    Parameters
	    ----------
	    message_new: str - name of new message to be sent to directory (i.e. getM or getS)
	    dest : str - name of destination entity of received message
	    src : str - name of source entity of received message 
	    msg_name: str - name of message that was received 
	    memory_addr: int - address of block being requested 
	    message: obj - full message that was received 

	    Returns
	    -------
	    None

		"""
		self.interconnect.send_message('directory', self.name, (message_new, memory_addr))
	
	def update_state(self, dest, src, msg_name, memory_addr, message):
		"""
	    updates state internally for requestor (particularly mode of cache block)

	    Parameters
	    ----------
	    dest : str - name of destination entity of message
	    src : str - name of source entity of message 
	    msg_name: str - name of message that was received 
	    memory_addr: int - address of block being requested 
	    message: obj - full message that was received 

	    Returns
	    -------
	    None

		"""
		mode = message[2][2]
		new_mode_value = message[2][3]
		self.requestor_arch.update_cache_state(memory_addr, mode, new_mode_value)

		#FOR TESTING
		self.local_cache_state[memory_addr] = new_mode_value

