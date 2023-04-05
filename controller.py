import inspect
import textwrap
from requestor.requestor_msi import requestor_msi
from invalidator.invalidator_msi import invalidator_msi
from directory.directory_msi import directory_msi
from cache_state import *
from requestor.requestor_arch import requestor_arch
from directory.directory_arch import directory_arch
from invalidator.invalidator_arch import invalidator_arch
from interconnect import interconnect
import time
import threading
import sys
import multiprocessing 



class controller(object):
	def __init__(self, interconnect, requestor, invalidator, directory, requestor_arch,invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
		self.requestor = requestor(interconnect, requestor_arch, directory, requestor_cache_state, name)
		self.invalidator = invalidator(interconnect, invalidator_arch, invalidator_cache_state, name)

