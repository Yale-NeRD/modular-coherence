
import time
import sys
sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
from framework.interconnect.interconnect import interconnect
from framework.test.controller import controller
from framework.requestor.requestor_arch import requestor_arch
from framework.directory.directory_arch import directory_arch
from framework.invalidator.invalidator_arch import invalidator_arch
import threading
import multiprocessing
import os

class test_environment(object):

    def __init__(self, shared_state, shared_state2, global_cache_state, request_address, request_type, correct_answer, directory_type, requestor_type, invalidator_type):
        self.controller_names = ["a1", "a2"]

        self.interconnect_object = interconnect(self.controller_names)
        self.requestor_arch1 = requestor_arch()
        self.invalidator_arch1 = invalidator_arch()
        self.dir_arch = directory_arch()
        self.directory = directory_type(
            self.interconnect_object, self.dir_arch, global_cache_state)

        # #two controllers that have requestor and invalidator
        self.a1 = controller(self.interconnect_object, requestor_type, invalidator_type,
                             self.requestor_arch1, self.invalidator_arch1, shared_state, shared_state, name="a1")
        self.a2 = controller(self.interconnect_object, requestor_type, invalidator_type,
                             self.requestor_arch1, self.invalidator_arch1, shared_state2, shared_state2, name="a2")

        self.request_address = request_address
        self.request_type = request_type
        self.correct_answer = correct_answer

        self.interconnect_object.controller_queues["a1"]["requestor"].append(
            ("a1", "application", (self.request_type, self.request_address)))
        self.thread_return = {"success": -1}

    def run_test(self, end=False):
        a1_req_thread = threading.Thread(target=self.a1.requestor.run, args=())
        a1_inval_thread = threading.Thread(
            target=self.a1.invalidator.run, args=())
        a2_req_thread = threading.Thread(target=self.a2.requestor.run, args=())
        a2_inval_thread = threading.Thread(
            target=self.a2.invalidator.run, args=())
        directory_thread = threading.Thread(target=self.directory.run, args=())
        x4 = threading.Thread(target=self.a1.requestor.run, args=())
        x5 = threading.Thread(target=self.directory.run, args=())
        x6 = threading.Thread(target=self.a1.requestor.debug_check_answer, args=(
            self.thread_return, self.request_address))
        a1_req_thread.daemon, a1_inval_thread.daemon, a2_req_thread.daemon, a2_inval_thread.daemon, directory_thread.daemon = True, True, True, True, True
        x4.daemon, x5.daemon, x6.daemon = True, True, True

        print("initialized interconnect - waiting 2 seconds...")
        time.sleep(2)

        a1_req_thread.start()
        a1_inval_thread.start()
        a2_req_thread.start()
        a2_inval_thread.start()
        directory_thread.start()

        time.sleep(10)

        x4.start()
        x5.start()
        time.sleep(10)
        x6.start()

        # check if state is correct in requestor
        if self.thread_return["success"] == self.correct_answer:
            print("PASSED TEST\n=====================")
        else:
            print("FAILED TEST\n=====================")

        if end == True:
            sys.exit()
