int get_stored_cache_line_mode(int memory_addr){
/* 	gets mode (i.e. modified, shared, invalid) for a stored cache line entry; 
	if cache line entry doesn't exist: return invalid)

	params:
	:memory_addr -  memory address of requested cache line 

	return:
	:mode: state/mode of the cache line being requested (i.e. M, O, E, S, I) */

	INSERT CODE HERE
}

int flush_cache_line_entry_to_network(int memory_addr){
/* 	params:
	:memory_addr - address of block that is being flushed */

	INSERT CODE HERE
}

int update_cache_line_state(int cache_line, int state, int new_value){
/* 	update cache line to a new_state (generally after response from network)

	params:
	:cache_line - cache entry for page
	:state - state that is being updated
	:new_value - new value for state */

	INSERT CODE HERE
}

int invalidate_cache_line_entry(int memory_addr, int new_mode){
/* 	given address, invalidate/change state/mode of the cache line entry that stores the memory_addr that has been requested

	params:
	:address - address of requested block
	:new_mode - new permissions mode for the requested block

	return:
	TODO */

		if ( data_required){
 			flush_page_to_network(memory_addr)
 		}
		if ( remove_data == True){
 			update_cache_state(cache_line, "mode", 0)
 		}
		if ( remove_data == False){
 			update_cache_state(cache_line, "mode", 1)
 }

