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

	def send_message(self, recipient, sender, message_name, arguments, invalidator=None):
		print("MESSAGE WAS SENT TO", recipient, "from", sender, "with contents:", message_name, arguments)
		time.sleep(2)
		if recipient == "directory":
			self.directory_queue.append((message_name, arguments, sender))
		elif recipient in self.controller_queues and invalidator == True:
			self.controller_queues[recipient]["invalidator"].append((message_name, arguments, sender))
		elif recipient in self.controller_queues and invalidator == False:
			self.controller_queues[recipient]["requestor"].append((message_name, arguments, sender))

		else:
			print("ERROR")

	def get_queue_element(self, name, invalidator=None):
		queue = None
		if name == "directory":
			queue = self.directory_queue 
		elif name in self.controller_queues and invalidator == True:
			queue = self.controller_queues[name]["invalidator"]
		elif name in self.controller_queues and invalidator == False:
			queue = self.controller_queues[name]["requestor"]
		else:
			print("ERROR")
			return

		if len(queue) != 0:
			request = queue.pop()
			# print("request received by", name, request)
			return request 
