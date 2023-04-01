class directory_arch(object):
	def __init__(self):
		pass
	def invalidate_sharers(self, sharers, memory_addr, new_mode):
		pass


	def get_data(self, memory_addr):
		print("DIRECTORY: directory_get_data(", memory_addr, ")")
		
	def update_directory_state(self, memory_addr, mode, new_mode_value):
		print("DIRECTORY: update_directory_state(", memory_addr, mode, new_mode_value,")")
		pass

	def get_directory_state(self, memory_addr, mode):
		print("DIRECTORY: get_directory_state(", memory_addr, mode,")")


	def store_request(self, requestor, memory_addr,new_state_requestor):
		print("DIRECTORY: store_request(", requestor, memory_addr, new_state_requestor,")")

	def get_request(self, memory_addr):
		print("DIRECTORY: get_request(", memory_addr, ")")
		return 0, 0 #REMOVE THIS
		#return requestor, and new_state_requestor







