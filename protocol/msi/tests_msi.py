import textwrap
import inspect
import sys, os
sys.path.append("/Users/aditgupta/Documents/cache_coherence/")
import time
from protocol.msi.cache_state_msi import *
import threading
import multiprocessing
from framework.test.test_environment import test_environment

from protocol.msi.requestor_msi import requestor_msi
from protocol.msi.invalidator_msi import invalidator_msi
from protocol.msi.directory_msi import directory_msi

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: INVALID}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0, "mode": INVALID, "sharers": []}  # a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: INVALID}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0, "mode": INVALID, "sharers": []}  # a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: MODIFIED}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": MODIFIED, "sharers": ["a2"]}  # a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: MODIFIED}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": MODIFIED, "sharers": ["a2"]}  # a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: SHARED}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": SHARED, "sharers": ["a2"]}  # a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: INVALID}  # a1 state
shared_state2 = {0: SHARED}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": SHARED, "sharers": ["a2"]}  # a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: SHARED}  # a1 state
shared_state2 = {0: SHARED}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0, "mode": SHARED,
                         "sharers": ["a1", "a2"]}  # a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: SHARED}  # a1 state
shared_state2 = {0: INVALID}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": SHARED, "sharers": ["a1"]}  # a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: MODIFIED}  # a1 state
shared_state2 = {0: INVALID}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": SHARED, "sharers": ["a1"]}  # a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0: MODIFIED}  # a1 state
shared_state2 = {0: INVALID}  # a2 state
global_cache_state = {}
global_cache_state[0] = {"data": 0,
                         "mode": SHARED, "sharers": ["a1"]}  # a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state,
                                        request_address, request_type, CORRECT_ANSWER, directory_msi, requestor_msi, invalidator_msi)
new_test_environment.run_test(end=True)
