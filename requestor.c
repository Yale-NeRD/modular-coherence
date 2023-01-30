char* get_data_from_cache_line(int memory_addr){
/* 	after knowing that the data exists, 
	return the data that is in the cache line for the processor's use. 

	params:
	:memory_addr (int) -  memory address of requested cache line 

	return:
	:data (str): the actual data from the cache_line */

	INSERT CODE HERE
}

int get_stored_cache_line_mode(int memory_addr){
/* 	gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
	if cache line entry doesn't exist: return invalid)

	params:
	:memory_addr -  memory address of requested cache line 

	return:
	:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I) */

	INSERT CODE HERE
}

int initialize_cache_entry(int memory_addr){
/* 	prepares a cache_entry before a request is made. Specifically, if:
	        - If cache entry doesn't exist for address, prepare cache entry for it (i.e. evict block)
	        - If cache entry exists, return True
	        - other cases error out (return False)

	params:
	:memory_addr - memory address of data being requested

	No return value */

	INSERT CODE HERE
}

int send_request_to_network(int address, int mode){
/* 	request cache line from network 

	params:
	:address - address of page desired 
	:mode (int) - request of M, O, E, S, I, etc. (should map to cache_entry_states)


	return:
	: mode: mode of address being returned  */

	INSERT CODE HERE
}

int update_cache_state(int memory_addr, char* state, int new_value){
/* 	update cache line to a new_state (generally after response from network)

	params:
	:memory_addr - address of requested block of data 
	:state - state that is being updated
	:new_value - new value for state */

	INSERT CODE HERE
}

char* get_cache_line_entry(int memory_addr, int requested_mode){
/* 	main function called by requestor

	params:
	:memory_addr (int) -  memory address of requested cache line 
	:requested_mode (int) - mode that the process is requesting data block in

	return:
	:data (str): the actual data from the cache line after it has been received */

		stored_cache_line_mode = get_stored_cache_line_mode(memory_addr)
 
 		if ( stored_cache_line_mode == MODIFIED){
 			return get_data_from_cache_line(memory_addr)
 		}
	
 		initialize_cache_entry(memory_addr)
 
 		if ( stored_cache_line_mode == SHARED && requested_mode != SHARED ){
 			send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
 		}
		if ( stored_cache_line_mode == INVALID){
 			send_request_to_network(address, requested_mode) #mode may be M, S, E, etc. 
 		}
		else if ( hi){
 			pass
 		}

 		update_cache_state(memory_addr, "mode", requested_mode)
 		return get_data_from_cache_line(memory_addr)
 }

