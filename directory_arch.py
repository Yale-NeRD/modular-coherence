class directory_arch(object):
	def __init__(self):
		pass
	def invalidate_sharers(self, sharers, memory_addr, new_mode):
		pass


	def get_data(self, memory_addr):
		print("directory_get_data(", memory_addr, ")")
		
	# def respond_to_requestor(self, requestor, memory_addr, data, modified):
	# 	pass
	def update_directory_state(self, memory_addr, state, new_state_value):
		print("update_directory_state(", memory_addr, state, new_state_value,")")
		pass





