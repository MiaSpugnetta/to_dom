from abstractions.database import update_entry, get_db_entries

all_db_entries = get_db_entries()

update = {'done': False}

for entry in all_db_entries:
    key = entry['key']
    update_entry(update, key)

#update_entry()