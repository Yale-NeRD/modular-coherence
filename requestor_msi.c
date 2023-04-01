char * interconnect__get_message(char* self_name, int* invalidator);
char * requestor_arch__get_current_cache_line_mode(char ** args);

int run(){
	message = interconnect__get_message(self_name, False);
	args = parse_message(message);
	current_state = get_current_state(args)

	if args["message_name"] == "read" && current_state == INVALID:
		interconnect_send_message('directory', self_name, ("getS", args["memory_addr"]))
	else if args["message_name"] == "write" && current_state == INVALID:
		interconnect_send_message('directory', self_name, ("getM", args["memory_addr"]))
	else if args["message_name"] == "read" && current_state == SHARED:
		interconnect_send_message('directory', self_name, ("getS", args["memory_addr"]))
	else if args["message_name"] == "change_state" && current_state == SHARED:
		requestor_arch_update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
	else if args["message_name"] == "change_state" && current_state == INVALID:
		requestor_arch_update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
	else if args["message_name"] == "change_state" && current_state == MODIFIED:
		requestor_arch_update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
}

int parse_message(char *message){

	TODO; write code to parse message

	return args;
}

int get_current_state(char ** args):
	int current_state = requestor_arch__get_current_cache_line_mode(args["memory_addr"]);
	return current_state;
