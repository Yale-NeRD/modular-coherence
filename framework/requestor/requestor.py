import inspect
import textwrap
import sys
sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
from framework.run_entity import run_entity


class requestor(run_entity):
    """
    requestor class that is inherited by specific requestor object classes that implement cache coherence protocol (i.e. requestor_msi)

    Specifically sets valid_messages that can be received, initializes match_action_table, name, and interconnect
        
    """
    def __init__(self, interconnect, requestor_arch, name):
        """
        init funciton to initialize requestor class 

        Parameters
        ----------
        interconnect : interconnect() object - from interconnect.py, it is interconnect object shared by invalidator, directory, and requestor
        requestor_arch: arch() object - kernel function defintions that are given to requestor (and will be filled in by arch developer)
        name: str - name of invalidator (this is stored in directory memory for cache coherence)

        """
        super(requestor, self).__init__(interconnect, False)

        self.requestor_arch = requestor_arch

        self.match_action_table = {}

        self.name = name

        self.valid_messages = ["change_state", "read", "write"]

        for msg in self.valid_messages:
            self.match_action_table[msg] = {}

        self.interconnect = interconnect


