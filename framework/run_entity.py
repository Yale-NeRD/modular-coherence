class run_entity(object):
    def __init__(self, interconnect, invalidator_bool):
        self.interconnect = interconnect
        self.invalidator = invalidator_bool
        self.match_action_table = {}

    def run(self):
        """
        main run() function that is automatically called from each entity; calls other subfunctions to call and complete match action table actions/functions

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        message = self.interconnect.get_message(
            self.name, invalidator=self.invalidator) #get message from interconnect queue if exists for entity 
        dest, src, msg_name, memory_addr, message = self.parse_message(message)
        current_state = self.get_current_state(memory_addr)
        ftn_list = self.get_match_action_table_entry(msg_name, current_state) 
        self.invoke_matched_function(
            ftn_list, dest, src, msg_name, memory_addr, message)

    def get_current_state(self, memory_addr):
        """
        gets current state of cache block for memory_addr in requestor entity 

        Parameters
        ----------
        memory_addr : int - address of block being requested 

        Returns
        -------
        int: current mode of cache block in requestor entity

        """
        pass #IMPLEMENTED BY HIGHER-LEVEL PROTOCOL 

    def parse_message(self, message):
        """
        parses message into five components: dest, src, message_name, memory_addr in question, and full message (non-decomposed)

        Parameters
        ----------
        message : message object (tuple) 

        Returns
        -------
        dest : str - name of destination entity of message
        src : str - name of source entity of  message 
        msg_name: str - name of message 
        memory_addr: int - address of block in question 
        message: obj - full message without parsing

        """
        dest = message[0]
        src = message[1]
        message_contents = message[2]
        msg_name = message_contents[0]
        memory_addr = message_contents[1]
        return dest, src, msg_name, memory_addr, message

    def get_match_action_table_entry(self, args, current_state):
        return self.match_action_table[args["message_name"]][current_state]

    def get_match_action_table_entry(self, msg_name, current_state):
        return self.match_action_table[msg_name][current_state]

    def invoke_matched_function(self, ftn_list, dest, src, msg_name, memory_addr, message):
        for ftn, param in ftn_list:
            new_param = param + [dest, src, msg_name, memory_addr, message]
            ftn(*tuple(new_param))  # this adds context, args to the param_list

    def debug_check_answer(self, thread_return, memory_addr):
        thread_return["success"] = self.local_cache_state[memory_addr]
        return
