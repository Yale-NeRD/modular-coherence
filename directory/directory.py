from run_entity import run_entity
import textwrap
import inspect
import sys
sys.path.insert(0, "..")

# from cache_state import *


class directory(run_entity):
    def __init__(self, interconnect, directory_arch):
        super(directory, self).__init__(interconnect, None)

        self.directory_arch = directory_arch

        self.valid_messages = ["getS", "getM", "ACK"]

        # make a table of size n x n states
        self.match_action_table = {}

        for msg in self.valid_messages:
            self.match_action_table[msg] = {}

        self.global_cache_state = {}
        #key = cache_addr
        #value = dict(data, mode, [sharers])

        self.interconnect = interconnect

        self.name = "directory"
