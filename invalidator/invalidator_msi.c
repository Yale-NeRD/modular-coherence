char * interconnect__get_message(char* self_name, int* invalidator);
char * invalidator_arch__get_current_cache_line_mode(char ** args);
int * invalidator_arch__flush_cache_line_entry_to_network();

int run(){
	message = interconnect__get_message(self_name, False);
	args = parse_message(message);
	current_state = get_current_state(args)

	if args["message_name"] == "change_state" && current_state == SHARED:
		invalidator_arch__update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"]);
		interconnect__send_message('directory', self_name, ("ACK", args["memory_addr"]));
	else if args["message_name"] == "change_state" && current_state == INVALID:
		invalidator_arch__update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"]);
		interconnect__send_message('directory', self.self_name, ("ACK", args["memory_addr"]));
	else if args["message_name"] == "change_state" && current_state == MODIFIED:
		invalidator_arch__update_cache_state(args["memory_addr"], args["mode"], args["new_mode_value"])
		invalidator_arch__flush_cache_line_entry_to_network(args["memory_addr"]);
		interconnect__send_message('directory', self_name, ("ACK", args["memory_addr"]));
}

int parse_message(char *message){

	TODO; write code to parse message

	return args;
}

int get_current_state(char ** args):
	int current_state = invalidator_arch__get_current_cache_line_mode(args["memory_addr"]);
	return current_state;
