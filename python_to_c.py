from requestor import requestor 
from invalidator import invalidator
import inspect
import textwrap


#USER DEFINED
convert_requestor = True #if True, then converts requestor, else converts invalidator to c source code 

if convert_requestor:
	requestor_main_method_name = "get_cache_line_entry"
	converted_class = requestor
	output_file_name = "requestor.c"
else:
	requestor_main_method_name = "invalidate_cache_line_entry"
	converted_class = invalidator	
	output_file_name = "invalidator.c"


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


function_names = []
with open(output_file_name, "a") as f:
	# print()
	# print(inspect.getmembers(converted_class, inspect.ismethod))
	for name, method in inspect.getmembers(converted_class, predicate=inspect.isfunction):
	    if callable(method):
	        method_name = method.__name__
	        if method_name == "__init__" or method_name == requestor_main_method_name:
	        	continue
	        else:
	        	write_function_definition_and_docstring(method, f)
	        	function_names.append(method_name)

	for name, method in converted_class.__dict__.items():    
		if callable(method):   
			method_name = method.__name__
			if method_name == requestor_main_method_name:
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