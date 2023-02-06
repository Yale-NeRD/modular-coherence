from invalidator import invalidator 
from requestor import requestor
from directory import directory 

#==========================================================================
# EXAMPLE 1
'''
	      A			(requestor, invalid) --> request: read
		   \
			D 		(directory)
		   /|\
		  C X Z		(invalidator, shared)

'''

# C = invalidator("C")
# X = invalidator("X")
# Z = invalidator("Z")
# D = directory()
# A = requestor(D)


# D.global_cache_state[0] = {"data":0, "mode": "shared", "sharers": [C, X, Z]}
# A.cache_state[0] = "invalid"
# C.cache_state[0] = "shared"
# X.cache_state[0] = "shared"
# Z.cache_state[0] = "shared"
# A.get_cache_line_entry(0, "read")

#==========================================================================
# EXAMPLE 2
'''
	      A			(requestor, invalid) --> request: write
		   \
			D 		(directory)
		   /
		  B 		(invalidator, modified)

'''

# B = invalidator("B")
# D = directory()
# A = requestor(directory=D)


# D.global_cache_state[0] = {"data":0, "mode": "modified", "sharers": [B]}
# A.cache_state[0] = "invalid"
# B.cache_state[0] = "modified"
# A.get_cache_line_entry(0, "write")


#==========================================================================
# EXAMPLE 3
'''
	      A			(requestor, invalid) --> request: read
		   \
			D 		(directory)
		   /
		  B 		(invalidator, modified)

'''

# B = invalidator("B")
# D = directory()
# A = requestor(directory=D)


# D.global_cache_state[0] = {"data":0, "mode": "modified", "sharers": [B]}
# A.cache_state[0] = "invalid"
# B.cache_state[0] = "modified"
# A.get_cache_line_entry(0, "read")

#==========================================================================
# EXAMPLE 4
'''
	      A			(requestor, modified) --> request: read
		   \
			D 		(directory)
		   /
		  B 		(invalidator, invalid)


		  output is ERROR, because requestor (A) already has the cache line entry

'''

B = invalidator("B")
D = directory()
A = requestor(directory=D)


D.global_cache_state[0] = {"data":0, "mode": "modified", "sharers": [A]}
A.cache_state[0] = "modified"
# B.cache_state[0] = "modified"
A.get_cache_line_entry(0, "read")


