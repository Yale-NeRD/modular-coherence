
import time
from controller import run_test
from cache_state import *

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:INVALID} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": INVALID, "sharers": []} #a3 state
request_address = 0
request_type = "read"
CORRECT_ANSWER = SHARED
run_test(shared_state, shared_state2, global_cache_state, request_address, request_type, CORRECT_ANSWER)


time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:MODIFIED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": 0, "sharers": ["a2", MODIFIED]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
run_test(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)


time.sleep(3)

shared_state = {0:INVALID} #a1 state
shared_state2 = {0:SHARED} #a2 state
global_cache_state = {}
global_cache_state[0] = {"data":0, "mode": 0, "sharers": ["a2", SHARED]} #a3 state
request_address = 0
request_type = "write"
CORRECT_ANSWER = MODIFIED
run_test(shared_state, shared_state2, global_cache_state, request_address, request_type,CORRECT_ANSWER)
