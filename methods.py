
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config



def capitalise_dict_values(dict_of_msgs):
    final_dict = dict_of_msgs.copy()  # Create copy of original dictionary

    for id,msg in final_dict.items():  # For key, value (where key=id and vale={msg}) in dictionary of messages:
        for k,field in msg.items():  # For key, value (where key='subject', 'text and values are the subject and text of the msg) in msg subdictionary:
            if k in ['subject']:  # If key == the str 'subject' (or if the k is contained (is equal to on of the entries) in the list that contains the str 'subject':
                msg[k] = msg[k].capitalize()  # Capitalise the value of the key 'subject'.
            # (Can also be represented as:
            #  For relevant_entry in relevant_list: # relevant_list = ['this', 'that', 'those']
            #    If k == relevant_entry:
            #        Do your thing)

        final_dict[id] = msg  # Overwrite the original msg in the original dict with the msg that contains the capitalised subject values.

    return final_dict