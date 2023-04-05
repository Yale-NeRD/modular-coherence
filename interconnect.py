import time


#note that the input controllers to the object is a list of names in controller.py (which initiates the entire process)
class interconnect(object):
	def __init__(self, controllers):
		self.directory_queue = []
		self.controller_queues = {}
		for controller in controllers:
			self.controller_queues[controller] = {}
			self.controller_queues[controller]["requestor"] = []
			self.controller_queues[controller]["invalidator"] = []

	def send_message(self, dest, src, message, invalidator=None):
		time.sleep(2)
		if dest == "directory":
			self.directory_queue.append((dest, src, message))
		elif dest in self.controller_queues and invalidator == True:
			self.controller_queues[dest]["invalidator"].append((dest, src, message))
		elif dest in self.controller_queues and invalidator == False:
			self.controller_queues[dest]["requestor"].append((dest, src, message))

		else:
			print("ERROR")


	def get_message(self, name, invalidator=False):
		queue = None
		if name == "directory":
			queue = self.directory_queue 
		elif name in self.controller_queues and invalidator == True:
			queue = self.controller_queues[name]["invalidator"]
		elif name in self.controller_queues and invalidator == False:
			queue = self.controller_queues[name]["requestor"]

		while(True):
			if len(queue) >= 1:
				message = queue.pop()
				# print("MESSAGE RECEIVED BY", name) #THIS iS PRINT STATEMNT THAT IS EVERYWHERE
				return message



