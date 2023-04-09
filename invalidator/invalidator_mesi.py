import sys
sys.path.insert(0,"..")


import inspect
import textwrap
from cache_state_mesi import *
from invalidator.invalidator import invalidator

class invalidator_mesi(invalidator):
	def __init__(self, interconnect, invalidator_arch, local_cache_state, name="a"):
		super(invalidator_mesi, self).__init__(interconnect, invalidator_arch, name)

		self.local_cache_state = local_cache_state

		self.match_action_table["change_state"][INVALID] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][SHARED] = [(self.update_state, []),
															(self.send_ack_to_dir, [])] 

		self.match_action_table["change_state"][MODIFIED] = [(self.update_state, []),
		                                                     (self.flush_cache_to_network, []),
															(self.send_ack_to_dir, [])]

		self.match_action_table["change_state"][EXCLUSIVE] = [(self.update_state, []),
															(self.send_ack_to_dir, [])]


	def get_current_state(self, memory_addr):
		"""
	    gets current state of cache block for memory_addr in invalidator entity 

	    Parameters
	    ----------
	    memory_addr : int - address of block being requested 

	    Returns
	    -------
	    int
	        current mode of cache block in invalidator entity

		"""
		current_state = self.invalidator_arch.get_stored_cache_line_mode(memory_addr)

		#FOR TESTING:
		current_state = INVALID
		if memory_addr in self.local_cache_state:
			current_state = self.local_cache_state[memory_addr]
		return current_state

	def flush_cache_to_network(self, dest, src, msg_name, memory_addr, message):
		"""
	    flushes cache block to full disaggregated network of controllers so that all can see it 

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
		self.invalidator_arch.flush_cache_line_entry_to_network(memory_addr)

	def send_ack_to_dir(self,  dest, src, msg_name, memory_addr, message):
		"""
	    sends an ack to directory from invalidator that it has acknowledged and completed the task asked by directory 

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
		self.interconnect.send_message('directory', self.name, ("ACK", memory_addr))

	def update_state(self, dest, src, msg_name, memory_addr, message):
		"""
	    updates state internally for invalidator (particularly mode of cache block)

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
		self.invalidator_arch.update_cache_state(memory_addr, mode, new_mode_value)

