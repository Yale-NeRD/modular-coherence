import inspect
import textwrap


###STATE DEFINITIONS###
MODIFIED = 2
SHARED = 1
INVALID = 0


class requestor():
	#cache entry states must be defined by cache coherence developer 
	def __init__(self):
		cache_entry_states = {
		"modified":2,
		"shared":1,
		"invalid":0
		}

	def get_cache_line_entry(self, memory_addr:int, requested_mode:int) -> str:
		'''
		main function called by requestor
		
		params:
		:memory_addr (int) -  memory address of requested cache line 
		:requested_mode (int) - mode that the process is requesting data block in

		return:
		:data (str): the actual data from the cache line after it has been received

		'''
		stored_cache_line_mode = self.get_stored_cache_line_mode(memory_addr)

		if stored_cache_line_mode == MODIFIED:
			return self.get_data_from_cache_line(memory_addr)
	
		self.initialize_cache_entry(memory_addr)

		if stored_cache_line_mode == SHARED and requested_mode != SHARED :
			self.send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
		if stored_cache_line_mode == INVALID:
			self.send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
		elif hi:
			pass

		self.update_cache_state(memory_addr, "mode", requested_mode)
		return self.get_data_from_cache_line(memory_addr)


	def get_data_from_cache_line(self, memory_addr: int) -> str:
		'''
		after knowing that the data exists, 
		return the data that is in the cache line for the processor's use. 
		
		params:
		:memory_addr (int) -  memory address of requested cache line 

		return:
		:data (str): the actual data from the cache_line

		'''
		pass

	def get_stored_cache_line_mode(self, memory_addr: int) -> int:
		'''
		gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
		if cache line entry doesn't exist: return invalid)

		params:
		:memory_addr -  memory address of requested cache line 

		return:
		:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I)

		'''
		return mode

		'''
		expected semantics for architecture developer:
			 - ensure that address exists in cache
		'''

	def initialize_cache_entry(self,memory_addr:int) -> int: #
		'''
		prepares a cache_entry before a request is made. Specifically, if:
			- If cache entry doesn't exist for address, prepare cache entry for it (i.e. evict block)
			- If cache entry exists, return True
			- other cases error out (return False)

		params:
		:memory_addr - memory address of data being requested

		No return value
		'''
		return None

		'''
		expected semantics for architecture developer:
			 - do same thing in description above 
		'''


	def send_request_to_network(self,address:int, mode:int) -> int: #is_read can just be mode (eg. M, O, E, S,...)
		'''
		request cache line from network 

		params:
		:address - address of page desired 
		:mode (int) - request of M, O, E, S, I, etc. (should map to cache_entry_states)

		
		return:
		: mode: mode of address being returned 
		'''
		pass
		# return response #from network  

		'''
		expected semantics for architecture developer:
			 - send request to network (i.e. the network RDMA)
		'''


	def update_cache_state(self, memory_addr:int, state:str, new_value:int) -> int:
		'''
		update cache line to a new_state (generally after response from network)

		params:
		:memory_addr - address of requested block of data 
		:state - state that is being updated
		:new_value - new value for state
		'''

		'''
		expected semantics for architecture developer:
			- The code needs to figure out the cache entry for the memory_addr
			- Then for the given state, must update the value (i.e. the mode may change from S --> M or I-->S)
		'''
		pass



'''
note for any given simple cache coherence protocol there are three options:
	1. read --> write
	2. invalid --> read
	3. invalid --> write
'''



###DO NOT CHANGE BELOW THIS

def def_get_function_name_if_exists(word):
	if word[:4] == "self":
		return word[5:]
	return word


#TODO get type for the equals case
def parser(line, function_names):
	# line = line.lstrip()
	split_line = line.split("\t")

	initial_tab = True
	tab_counter = 0
	for word in split_line:
		if word == "" and initial_tab == True:
			tab_counter += 1
		else:
			initial_tab = False
	if len(split_line) > tab_counter: #this means there was actual code in the line

		actual_line_of_code = split_line[tab_counter]
		split_actual_line_of_code = actual_line_of_code.split(" ")
		final_statement = ""
		in_if_statement = False

		if split_actual_line_of_code[0] in ["if", "elif"]:
			if split_actual_line_of_code[0] == "elif":
				split_actual_line_of_code[0] = "else if"

			split_actual_line_of_code[0] += " ("

			for index in range(len(split_actual_line_of_code)):
				if split_actual_line_of_code[index] == "and":
					split_actual_line_of_code[index] = "&&"
				elif split_actual_line_of_code[index] == "or":
					split_actual_line_of_code[index] = "||"


			for word in split_actual_line_of_code:
				final_statement += word + " "

			final_statement = final_statement.replace(':', "){") #change ending of string
			in_if_statement = True

		# elif "=" in actual_line_of_code:

		# 	pass
		elif split_actual_line_of_code[0] == "return":
			final_statement = "return "
			for word in split_actual_line_of_code[1:]:
				final_statement += def_get_function_name_if_exists(word) + " "

		else:
			for word in split_actual_line_of_code:
				final_statement += def_get_function_name_if_exists(word) + " "
		

		return tab_counter * "\t" + final_statement, tab_counter, in_if_statement

		
	else: 
		#there is just spaces (no actual code), so return the line immediately
		return line

def get_function_source_code(method):
	lines = inspect.getsourcelines(method)[0]
	source_code = []
	collect_code = False
	counter = 0
	for line in lines:
		if line.startswith('\t\t\'\'\''):
			counter += 1
		if collect_code == True:
			source_code.append(line)
		if counter == 2:
			collect_code = True
	return source_code


def write_function_definition_and_docstring(method, f, c_src_lines = None):
	parameter_string = ""

	arg_types = inspect.getfullargspec(method).annotations
	for arg in inspect.getfullargspec(method).args:
		if arg == "self":
			pass
		else:
			if parameter_string != "":
				parameter_string += ", " #add next parameter to function definition
			arg_type = arg_types[arg].__name__
			if arg_type == "str":
				arg_type = "char*" 
			parameter_string += str(arg_type) + " " + arg

	return_type = arg_types["return"].__name__
	if return_type == "str":
		return_type = "char*"

	doc_string = inspect.getdoc(method) # get's full documentation associated with the string 

	f.write(return_type + " " + method_name + "(" + parameter_string + ")" + "{" + "\n")
	f.write("/* " + textwrap.indent(doc_string, '\t') + " */" + 2*"\n")
	if c_src_lines != None:
		f.write(c_src_lines)
	else:
		f.write(textwrap.indent("INSERT CODE HERE", '\t') + "\n")
	f.write("}" + 2*"\n")


# x = requestor()
function_names = []
with open("requestor.c", "a") as f:
	for name, method in requestor.__dict__.items():
	    if callable(method):
	        method_name = method.__name__
	        if method_name == "__init__" or method_name == "get_cache_line_entry":
	        	continue
	        else:
	        	write_function_definition_and_docstring(method, f)
	        	function_names.append(method_name)

	for name, method in requestor.__dict__.items():    
		if callable(method):   
			method_name = method.__name__
			if method_name == "get_cache_line_entry":
				source_code = get_function_source_code(method)

				c_src_lines = ""
				if_statement = False
				if_tab_count = -1
				for line in source_code:
					line, tab_count, in_if_statement = parser(line, function_names)
					if if_statement == True and tab_count <= if_tab_count:
						c_src_lines += if_tab_count * "\t" + "}\n"
						if_statement = False

					if in_if_statement == True:
						if_statement = True
						if_tab_count = tab_count
					c_src_lines += line

				write_function_definition_and_docstring(method, f, c_src_lines)
				break







        		
        

















