
import time
# from controller import run_test
from cache_state import *
import sys

import threading
import multiprocessing 
import os
from test_environment import test_environment

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": INVALID, "sharers": []} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": INVALID, "sharers": []} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:MODIFIED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": MODIFIED, "sharers": ["a2"]} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:MODIFIED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": MODIFIED, "sharers": ["a2"]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:SHARED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a2"]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()


time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:SHARED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a2"]} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()


time.sleep(3)

shared_state = {0:SHARED} #a1 state
shared_state2 = {0:SHARED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a1", "a2"]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()


time.sleep(3)

shared_state = {0:SHARED} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a1"]} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()

time.sleep(3)

shared_state = {0:MODIFIED} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a1"]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test()


time.sleep(3)

shared_state = {0:MODIFIED} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": SHARED, "sharers": ["a1"]} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = MODIFIED
new_test_environment = test_environment(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
new_test_environment.run_test(end=True)




