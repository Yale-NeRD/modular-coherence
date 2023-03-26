# import inspect
# import textwrap
# from requestor_msi import requestor_msi
# from invalidator_msi import invalidator_msi
# from directory_msi import directory_msi
# from cache_state import *
# from requestor_arch import requestor_arch
# from directory_arch import directory_arch
# from invalidator_arch import invalidator_arch
# from interconnect import interconnect
# import time
# import threading
# import sys



# class controller(object):
# 	def __init__(self, interconnect, requestor, invalidator, directory, requestor_arch,invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
# 		self.requestor = requestor(interconnect, requestor_arch, directory, requestor_cache_state, name)
# 		self.invalidator = invalidator(interconnect, invalidator_arch, invalidator_cache_state, name)


# controller_names = ["a1", "a2"]

# #initialize all architectures 
# interconnect = interconnect(controller_names)
# requestor_arch1 = requestor_arch()
# invalidator_arch1 = invalidator_arch()
# dir_arch = directory_arch()
# directory = directory_msi(interconnect, dir_arch)


# #initialize initial block states
# shared_state = {0:INVALID}
# shared_state2 = {0:INVALID}




# #two controllers that have requestor and invalidator
# a1 = controller(interconnect, requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1,shared_state, shared_state, name="a1")
# a2 = controller(interconnect, requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1, shared_state2, shared_state2, name="a2")

# #directory state
# directory.global_cache_state[0] = {"data":0, "mode": INVALID, "sharers": []}



# #request by one controller to a cache line entry


# x1 = threading.Thread(target=a1.requestor.read_queue)
# x2 = threading.Thread(target=directory.collect_and_respond_requests)
# x3 = threading.Thread(target=a2.invalidator.invalidate_cache_line_entry)
# #daemon added to use sys.exit
# x1.daemon = True
# x2.daemon = True
# x3.daemon = True

# print(interconnect.directory_queue)
# x1.start()
# x2.start()
# x3.start()
# print("initialized interconnect - waiting 3 seconds...")
# time.sleep(3)

# a1.requestor.get_cache_line_entry(0, "read")
# print("sent request")

# time.sleep(10)
# sys.exit()


import inspect
import textwrap
from requestor_msi import requestor_msi
from invalidator_msi import invalidator_msi
from directory_msi import directory_msi
from cache_state import *
from requestor_arch import requestor_arch
from directory_arch import directory_arch
from invalidator_arch import invalidator_arch
from interconnect import interconnect
import time
import threading
import sys
import multiprocessing 

# CORRECT_ANSWER = INVALID


class controller(object):
	def __init__(self, interconnect, requestor, invalidator, directory, requestor_arch,invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
		self.requestor = requestor(interconnect, requestor_arch, directory, requestor_cache_state, name)
		self.invalidator = invalidator(interconnect, invalidator_arch, invalidator_cache_state, name)




#request by one controller to a cache line entry

def run_test(shared_state, shared_state2, global_cache_state,request_address, request_type, CORRECT_ANSWER):
	controller_names = ["a1", "a2"]

	#initialize all architectures 
	interconnect_object = interconnect(controller_names)
	requestor_arch1 = requestor_arch()
	invalidator_arch1 = invalidator_arch()
	dir_arch = directory_arch()
	directory = directory_msi(interconnect_object, dir_arch)

	CORRECT_ANSWER = CORRECT_ANSWER



	#two controllers that have requestor and invalidator
	a1 = controller(interconnect_object, requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1,shared_state, shared_state, name="a1")
	a2 = controller(interconnect_object, requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1, shared_state2, shared_state2, name="a2")

	directory.global_cache_state = global_cache_state


	#thread_return is only used for tests.py to check if the output state in the requestor matches the correct answer; can be deleted
	thread_return={'success': -1}


	x1 = threading.Thread(target=a1.requestor.read_queue, args=(thread_return,))
	x2 = threading.Thread(target=directory.collect_and_respond_requests)
	x3 = threading.Thread(target=a2.invalidator.invalidate_cache_line_entry)
	#daemon added to use sys.exit
	x1.daemon = True
	x2.daemon = True
	x3.daemon = True

	# print(interconnect_object.directory_queue)
	x1.start()
	x2.start()
	x3.start()
	print("initialized interconnect - waiting 3 seconds...")
	time.sleep(3)

	a1.requestor.get_cache_line_entry(request_address, request_type)
	print("sent request")

	time.sleep(10)

	if thread_return["success"] == CORRECT_ANSWER: #check if state is correct in requestor
		print("PASSED TEST\n=====================")
	else:
		print("FAILED TEST\n=====================")
	# sys.exit()

