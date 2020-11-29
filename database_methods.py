

# Function to add the messages to the database
def add_to_db(dict_of_msgs, db):
    for id, msg in dict_of_msgs.items():
        db.put(msg, key=str(id))