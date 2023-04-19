import textwrap
import inspect
import sys, os
sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
from protocol.msi.cache_state_msi import *
from framework.directory.directory import directory


class directory_msi(directory):
    def __init__(self, interconnect, directory_arch, directory_cache_state):
        super(directory_msi, self).__init__(interconnect, directory_arch)

        self.requests = {}

        self.directory_cache_state = directory_cache_state

        self.match_action_table["getS"][INVALID] = [
            (self.respond_to_requestor_immediate, [SHARED, True])]

        self.match_action_table["getM"][INVALID] = [
            (self.respond_to_requestor_immediate, [MODIFIED, True])]

        self.match_action_table["getS"][SHARED] = [
            (self.respond_to_requestor_immediate, [SHARED, False])]

        # these should be directory arch functions in general
        self.match_action_table["getM"][SHARED] = [
            (self.invalidate_sharers, [INVALID, MODIFIED])]

        # these should be directory arch functions in general
        self.match_action_table["getS"][MODIFIED] = [
            (self.invalidate_sharers, [SHARED, SHARED])]

        # these should be directory arch functions in general, but for simulation this works
        self.match_action_table["getM"][MODIFIED] = [
            (self.invalidate_sharers, [INVALID, MODIFIED])]

        self.match_action_table["ACK"][INVALID] = []
        self.match_action_table["ACK"][SHARED] = [
            (self.respond_to_requestor_after_invalidator, [])]
        self.match_action_table["ACK"][MODIFIED] = [
            (self.respond_to_requestor_after_invalidator, [])]

    def respond_to_requestor_immediate(self, new_state, update_directory_internal_state, dest, src, msg_name, memory_addr, message):
        """
    sends response message to requestor immediately without talking to any sharers (or performing invalidation) 

    Parameters
    ----------
    new_state: str - new mode for requestor to update state for cache block
    update_directory_internal_state: bool: True/False to update state internally (or not for already shared)
    dest : str - name of destination entity of received message
    src : str - name of source entity of received message 
    msg_name: str - name of message that was received 
    memory_addr: int - address of block being requested 
    message: obj - full message that was received 

    Returns
    -------
    None

        """
        data = self.directory_arch.get_data(memory_addr)
        if update_directory_internal_state:
            self.directory_arch.update_directory_state(
                memory_addr, 'mode', new_state)
        self.directory_arch.update_directory_state(memory_addr, 'sharers', src)
        self.interconnect.send_message(
            src, 'directory', ('change_state', memory_addr, "mode", new_state), False)

    def respond_to_requestor_after_invalidator(self, dest, src, msg_name, memory_addr, message):
        """
    sends response message after receiving acks by sharers (and/or performing invalidation) 

    Parameters
    ----------
    dest : str - name of destination entity of received message
    src : str - name of source entity of received message 
    msg_name: str - name of message that was received 
    memory_addr: int - address of block being requested 
    message: obj - full message that was received 

    Returns
    -------
    None

        """
        requestor, new_state_requestor = self.directory_arch.get_request(
            memory_addr)  # get request

        # FOR SAKE OF TESITNG, CAN BE REMOVED IN FUTURE
        requestor, new_state_requestor = self.requests[memory_addr]

        self.directory_arch.update_directory_state(
            memory_addr, 'mode', new_state_requestor)
        self.directory_arch.update_directory_state(
            memory_addr, 'sharers', requestor)
        self.interconnect.send_message(
            requestor, 'directory', ('change_state', memory_addr, "mode", new_state_requestor), False)

    def get_current_state(self, memory_addr):
        """
    gets current state of cache block for memory_addr in directoruy entity 

    Parameters
    ----------
    memory_addr : int - address of block being requested 

    Returns
    -------
    int
        current mode of cache block in requestor entity

        """

        # FOR TESTING:
        # current_state = SHARED
        current_state = INVALID
        if memory_addr in self.directory_cache_state:
            current_state = self.directory_cache_state[memory_addr]["mode"]
        return current_state

    def invalidate_sharers(self, new_state_invalidator, new_state_requestor, dest, src, msg_name, memory_addr, message):
        """
    sends invalidation requests to sharers of a given memory block 

    Parameters
    ----------
    new_state_invalidator: int - new state for invalidator entities toupdate cache block
    new_state_requestor: int - new state to update cache block for requestor 
    dest : str - name of destination entity of received message
    src : str - name of source entity of received message 
    msg_name: str - name of message that was received 
    memory_addr: int - address of block being requested 
    message: obj - full message that was received 

    Returns
    -------
    None

        """
        self.directory_arch.store_request(
            src, memory_addr, new_state_requestor)  # store request
        sharers = self.directory_arch.get_directory_state(
            memory_addr, "sharers")

        # FOR TESTING:
        self.requests[memory_addr] = (src, new_state_requestor)
        sharers = self.directory_cache_state[memory_addr]["sharers"]
        for sharer in sharers:
            self.interconnect.send_message(
                sharer, "directory", ("change_state", memory_addr, "mode", new_state_invalidator), True)

    def get_data(self, dest, src, msg_name, memory_addr, message):
        """
        get data from main memory for given memory_addr

    Parameters
    ----------
    dest : str - name of destination entity of received message
    src : str - name of source entity of received message 
    msg_name: str - name of message that was received 
    memory_addr: int - address of block being requested 
    message: obj - full message that was received 

    Returns
    -------
    data object

        """
        return self.directory_arch.get_data(memory_addr)
