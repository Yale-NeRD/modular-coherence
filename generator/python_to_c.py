from requestor_msi import requestor_msi
from requestor import requestor
from invalidator import invalidator
import inspect
import textwrap
import inspect
import textwrap
from requestor_msi import requestor_msi
from invalidator_msi import invalidator_msi
from directory_msi import directory_msi
# from cache_state import *
from requestor_arch import requestor_arch
from directory_arch import directory_arch
from invalidator_arch import invalidator_arch
from interconnect import interconnect
import time
import threading
import sys
import multiprocessing


# USER DEFINED
# convert_requestor = True #if True, then converts requestor, else converts invalidator to c source code

# if convert_requestor:
# 	requestor_main_method_name = "get_cache_line_entry"
# 	converted_class = requestor
# 	output_file_name = "requestor.c"
# else:
# 	requestor_main_method_name = "invalidate_cache_line_entry"
# 	converted_class = invalidator
# 	output_file_name = "invalidator.c"


# def def_get_function_name_if_exists(word):
# 	if word[:4] == "self":
# 		return word[5:]
# 	return word


# #TODO get type for the equals case
# def parser(line, function_names):
# 	# line = line.lstrip()
# 	split_line = line.split("\t")

# 	initial_tab = True
# 	tab_counter = 0
# 	for word in split_line:
# 		if word == "" and initial_tab == True:
# 			tab_counter += 1
# 		else:
# 			initial_tab = False
# 	if len(split_line) > tab_counter: #this means there was actual code in the line

# 		actual_line_of_code = split_line[tab_counter]
# 		split_actual_line_of_code = actual_line_of_code.split(" ")
# 		final_statement = ""
# 		in_if_statement = False

# 		if split_actual_line_of_code[0] in ["if", "elif"]:
# 			if split_actual_line_of_code[0] == "elif":
# 				split_actual_line_of_code[0] = "else if"

# 			split_actual_line_of_code[0] += " ("

# 			for index in range(len(split_actual_line_of_code)):
# 				if split_actual_line_of_code[index] == "and":
# 					split_actual_line_of_code[index] = "&&"
# 				elif split_actual_line_of_code[index] == "or":
# 					split_actual_line_of_code[index] = "||"


# 			for word in split_actual_line_of_code:
# 				final_statement += word + " "

# 			final_statement = final_statement.replace(':', "){") #change ending of string
# 			in_if_statement = True

# 		# elif "=" in actual_line_of_code:

# 		# 	pass
# 		elif split_actual_line_of_code[0] == "return":
# 			final_statement = "return "
# 			for word in split_actual_line_of_code[1:]:
# 				final_statement += def_get_function_name_if_exists(word) + " "

# 		else:
# 			for word in split_actual_line_of_code:
# 				final_statement += def_get_function_name_if_exists(word) + " "


# 		return tab_counter * "\t" + final_statement, tab_counter, in_if_statement


# 	else:
# 		#there is just spaces (no actual code), so return the line immediately
# 		return line

def get_function_source_code(method):
    lines = inspect.getsourcelines(method)[0]
    source_code = []
    # collect_code = False
    # counter = 0
    for line in lines:
        # 	if line.startswith('\t\t\'\'\''):
        # 		counter += 1
        # 	if collect_code == True:
        test = ' '.join(line.split())
        source_code.append(test)
    # 	if counter == 2:
    # 		collect_code = True
    return source_code


# def write_function_definition_and_docstring(method, f, c_src_lines = None):
# 	parameter_string = ""

# 	arg_types = inspect.getfullargspec(method).annotations
# 	for arg in inspect.getfullargspec(method).args:
# 		if arg == "self":
# 			pass
# 		else:
# 			if parameter_string != "":
# 				parameter_string += ", " #add next parameter to function definition
# 			arg_type = arg_types[arg].__name__
# 			if arg_type == "str":
# 				arg_type = "char*"
# 			parameter_string += str(arg_type) + " " + arg

# 	return_type = arg_types["return"].__name__
# 	if return_type == "str":
# 		return_type = "char*"

# 	doc_string = inspect.getdoc(method) # get's full documentation associated with the string

# 	f.write(return_type + " " + method_name + "(" + parameter_string + ")" + "{" + "\n")
# 	f.write("/* " + textwrap.indent(doc_string, '\t') + " */" + 2*"\n")
# 	if c_src_lines != None:
# 		f.write(c_src_lines)
# 	else:
# 		f.write(textwrap.indent("INSERT CODE HERE", '\t') + "\n")
# 	f.write("}" + 2*"\n")


# controller_names = ["a1", "a2"]
# shared_state = {0:INVALID} #a1 state
# shared_state2 = {0:INVALID} #a2 state
# global_cache_state = {}
# global_cache_state[0] = {"data":0, "mode": INVALID, "sharers": []} #a3 state
# request_address = 0
# request_type = "read"

# interconnect_object = interconnect(controller_names)
# requestor_arch1 = requestor_arch()
# invalidator_arch1 = invalidator_arch()
# dir_arch = directory_arch()
# directory = directory_msi(interconnect_object, dir_arch)

# class controller(object):
# 	def __init__(self, interconnect, requestor, invalidator, directory, requestor_arch,invalidator_arch, requestor_cache_state, invalidator_cache_state, name):
# 		self.requestor = requestor(interconnect, requestor_arch, directory, requestor_cache_state, name)
# 		self.invalidator = invalidator(interconnect, invalidator_arch, invalidator_cache_state, name)

# #two controllers that have requestor and invalidator
# a1 = controller(interconnect_object, requestor_msi, invalidator_msi, directory, requestor_arch1, invalidator_arch1,shared_state, shared_state, name="a1")

# requestor_obj = a1.requestor
# invalidator_obj = a1.invalidator

# for message in requestor_obj.valid_messages:
# 	for state in requestor_obj.valid_states:

# 		source_code = get_function_source_code(method)


# x = requestor_msi(None, None, None, None, None)
print(a1.requestor.match_action_table)

# interconnect, requestor_arch,directory, name


# with open(output_file_name, "a") as f:
# print()
# print(inspect.getmembers(converted_class, inspect.ismethod))
# for name, method in inspect.getmembers(converted_class, predicate=inspect.isfunction):
#     if callable(method):
#         method_name = method.__name__
#         if method_name == "run":
#         	source_code = get_function_source_code(method)
#         	print(source_code)

#         	for line in source_code:
#         			print(line)
#         	continue

# print("NOT HERE", method_name)
# 	write_function_definition_and_docstring(method, f)
# 	function_names.append(method_name)

# for name, method in converted_class.__dict__.items():
# 	if callable(method):
# 		method_name = method.__name__
# 		if method_name == requestor_main_method_name:
# 			source_code = get_function_source_code(method)

# 			c_src_lines = ""
# 			if_statement = False
# 			if_tab_count = -1
# 			for line in source_code:
# 				line, tab_count, in_if_statement = parser(line, function_names)
# 				if if_statement == True and tab_count <= if_tab_count:
# 					c_src_lines += if_tab_count * "\t" + "}\n"
# 					if_statement = False

# 				if in_if_statement == True:
# 					if_statement = True
# 					if_tab_count = tab_count
# 				c_src_lines += line

# 			write_function_definition_and_docstring(method, f, c_src_lines)
# 			break
