

class directory_arch(object):
	def __init__(self):
		pass
	def invalidate_sharers(self, sharers, memory_addr, new_mode):
		for sharer in sharers:
			print("directory_invalidating_sharer_" + sharer.invalidator.name)
			# print(sharer.invalidator)
			sharer.invalidator.invalidate_cache_line_entry(memory_addr, new_mode)

	def get_data(self, memory_addr):
		pass
	def respond_to_requestor(self, requestor, memory_addr, data, modified):
		pass
	def update_directory_state(self, memory_addr, data, mode, new_mode_value):
		pass





