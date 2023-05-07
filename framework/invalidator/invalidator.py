import textwrap
import inspect
import sys
sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
from framework.run_entity import run_entity

class invalidator(run_entity):
    """
    invalidator class that is inherited by specific invalidator object classes that implement cache coherence protocol (i.e. invalidator_msi)

    Specifically sets valid_messages that can be received, initializes match_action_table, name, and interconnect
        
    """
    def __init__(self, interconnect, invalidator_arch, name="a"):
        """
        init funciton to initialize invalidator class 

        Parameters
        ----------
        interconnect : interconnect() object - from interconnect.py, it is interconnect object shared by invalidator, directory, and requestor
        invalidator_arch: arch() object - kernel function defintions that are given to invalidator (and will be filled in by arch developer)
        name: str - name of invalidator (this is stored in directory memory for cache coherence)

        """
        super(invalidator, self).__init__(interconnect, True)

        self.name = name

        self.invalidator_arch = invalidator_arch

        self.valid_messages = ["change_state"]

        self.match_action_table = {}

        for msg in self.valid_messages:
            self.match_action_table[msg] = {}

        self.interconnect = interconnect
