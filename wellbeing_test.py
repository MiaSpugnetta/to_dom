from abstractions.database import get_db_entries
from _datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from collections import defaultdict
import operator
import itertools


# Function to convert the date string to type datetime object
def change_date_format(entries):
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            entry['date'] = datetime.strptime(entry['date'], '%a, %d %b %Y %H:%M:%S %z').date()
            #print(entry['date'])
            #print("*******")
    return entries

#########################################################################

# TODO: it returns a dict of form {'T': {'date': datetime.date(2021, 4, 15), 'score': 6.5}, 'M': {'date': datetime.date(2021, 4, 15), 'score': 4.5}}, it rewrites the score every time. FIX
def get_scores(entries):
    scores = {}
    li_wellbeing_entries = []

    # Create a list of dictionaries (entries) that are relevant
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            #print(entry)  # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '648', 'subject': 'Wellbeing', 'text': '9.5\r\n\r\n-- \r\nThomas Rost\r\n', 'user': 'T'}
            li_wellbeing_entries.append(entry)

    # print(li_wellbeing_entries)  # [
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '648', 'subject': 'Wellbeing', 'text': '9.5\r\n\r\n-- \r\nThomas Rost\r\n', 'user': 'T'},
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '654', 'subject': 'Wellbeing', 'text': '8\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '656', 'subject': 'Wellbeing', 'text': '8\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '657', 'subject': 'Wellbeing', 'text': "6.5 (tummy, don't want to work)\r\n", 'user': 'T'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '658', 'subject': 'Wellbeing', 'text': '7.5\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '659', 'subject': 'Wellbeing', 'text': '4.5\r\n', 'user': 'M'}]


    li_wellbeing_entries = sorted(li_wellbeing_entries, key=operator.itemgetter("date", "user"))  # sort the list that already exists by date and then by user

    #################################################

    # take the score of every entry, make it a float and create dict with the float(score), date and user
    scores_dict = defaultdict(list)

    for entrydict in li_wellbeing_entries:

        entry_text = entrydict['text'].split(" ")
        #print(entry_text)  #['9.5\r\n\r\n--', '\r\nThomas', 'Rost\r\n']

        score = entry_text[0].split("\r")
        score = float(score[0])

        # good till here

        #li_scores.append(entrydict['date'])
        #append_dict = {entrydict['user']: score}
        #li_scores.append(append_dict)


        append_dict = {entrydict['user']:[score]}

        scores_dict[entrydict['date']].append(append_dict)

        #print(append_dict)
        #print("__________________________")
        #print(scores_dict)

        #scores[entrydict['date']] = {'user': entrydict['user'], 'score': score}

        #scores[entrydict['date']] = [{entrydict['user']: score}]

    print(scores_dict)  # defaultdict(<class 'list'>{
    # datetime.date(2021, 4, 14): [
    #                               {'M': [8.0]},
    #                               {'M': [8.0]},
    #                               {'T': [9.5]}
    #                             ],
    # datetime.date(2021, 4, 15): [
    #                               {'M': [7.5]},
    #                               {'M': [4.5]},
    #                               {'T': [6.5]}
    #                              ]
    # })

    #print(pd.DataFrame.from_records(scores_dict))



    print("end of get_score()")
    return scores_dict
    #return tmp


entries = get_db_entries()
change_date_format(entries)

scores = get_scores(entries)
print(scores)
print("FUCK")
print(len(scores))
scores = dict(scores)
print(type(scores))
#print(scores.keys())
print("&&&&&&&&&&&&&")
#print(type(scores['T']['date']))
#print((scores['T']['date']))


#continue here

# Plot the stuff here
# TODO: make simple plot of the scores
for key,value in scores.items():
    for item in value:
        print(item)






# Create pandas DataFrame
#index_df =
score_df = pd.DataFrame.from_dict(scores)#, orient='index')#, orient=scores.keys())
#score_df = pd.Series(scores).apply(pd.Series).T
print(score_df)


def parse_dict_scores(dict_scores):
    return_dict = defaultdict(list) #{}

    for user in dict_scores:
        #append_dict = {
        #                'user': user,
        #                'score': dict_scores[user]['score']
        #}

        append_dict = {user: dict_scores[user]['score']}

        return_dict[dict_scores[user]['date']].append(append_dict)
    return return_dict


parsed_scores = parse_dict_scores(scores)
#print(parsed_scores)
#print(pd.DataFrame.from_records(parsed_scores))

print(f"this is the parsed_dict_scores: {parsed_scores} ***************")

dates = []
frames = []

for date, listuserscore in parsed_scores.items():
    dates.append(date)
    print(dates)
    for userscore in listuserscore:
        print(userscore)
        print(type(userscore))
        mini_df = pd.DataFrame(userscore, index=[0])
        print(mini_df)
        frames.append(mini_df)
        print(frames)

        #frames.append(pd.DataFrame(userscore, index=[0]))#, index=userscore))#, index=userscore.keys()))

        #frames.append(pd.DataFrame(userscore))#, index=userscore))#, orient='index'))


dataf = pd.concat(frames, keys=dates)

print("*************************************")
print(dataf)


#parsed_score_df = pd.DataFrame.from_dict({(i,j): parsed_scores[i][j] for i in parsed_scores.keys() for j in parsed_scores[i].keys()}, orien='index')


#parsed_score_df = pd.DataFrame.from_dict(parse_dict_scores(scores))

#print(parsed_score_df)

# Plot DataFrame
#plt.plot(score_df)

