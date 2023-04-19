import inspect
import textwrap

import time
import threading
# import sys
# sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
# from framework.interconnect.interconnect import interconnect
import multiprocessing


class controller(object):
    def __init__(self, interconnect, requestor, invalidator, requestor_arch, invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
        self.requestor = requestor(
            interconnect, requestor_arch, requestor_cache_state, name)
        self.invalidator = invalidator(
            interconnect, invalidator_arch, invalidator_cache_state, name)
