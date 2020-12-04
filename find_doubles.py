from abstractions.database import *
from abstractions.configuration_path import *
#remove_double_entries()

all_entries = get_db_entries()
print(f'this is the # in db: {len(all_entries)}')

json_dict = load_from_file('msg_dict.json')
print(f'this is the # in json_file: {len(json_dict)}')

all_txt = []

for dict in json_dict:
    all_txt.append(json_dict[dict]['text'])

print(f'this is the # of just text elem in json file: {len(all_txt)}')
#wtf_list = []

#print(all_entries)
print("%%%%%%%%%%%%%%%%")
#print(all_txt)

what = 0
for entry in all_entries:
    for txt in all_txt:
        if entry['text'] != txt:
            #wtf_list.append(entry)
            what +=1
#print(len(wtf_list))
#print(wtf_list)

print(what)