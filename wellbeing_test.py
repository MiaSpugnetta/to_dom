from abstractions.database import get_db_entries
from _datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from collections import defaultdict
import operator
import itertools


# Function to convert the date string to type datetime object:
def change_date_format(entries):
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            entry['date'] = datetime.strptime(entry['date'], '%a, %d %b %Y %H:%M:%S %z').date()

    return entries


#########################################################################
# Function that returns a parsed defaultdict with the data
def get_scores(entries):

    # Create a list of dictionaries (entries) that are relevant:
    li_wellbeing_entries = []

    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            #print(entry)  # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '648', 'subject': 'Wellbeing', 'text': '9.5\r\n\r\n-- \r\nThomas Rost\r\n', 'user': 'T'}
            li_wellbeing_entries.append(entry)

    # li_wellbeing_entries structures as following:
    # li_wellbeing_entries = [
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '648', 'subject': 'Wellbeing', 'text': '9.5\r\n\r\n-- \r\nThomas Rost\r\n', 'user': 'T'},
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '654', 'subject': 'Wellbeing', 'text': '8\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 14), 'done': False, 'key': '656', 'subject': 'Wellbeing', 'text': '8\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '657', 'subject': 'Wellbeing', 'text': "6.5 (tummy, don't want to work)\r\n", 'user': 'T'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '658', 'subject': 'Wellbeing', 'text': '7.5\r\n', 'user': 'M'},
    # {'date': datetime.date(2021, 4, 15), 'done': False, 'key': '659', 'subject': 'Wellbeing', 'text': '4.5\r\n', 'user': 'M'}
    #                       ]

    li_wellbeing_entries = sorted(li_wellbeing_entries, key=operator.itemgetter("date", "user"))  # sort the list that already exists by date and then by user

    #################################################
    # Take the score of every entry, make it a float and return a  defaultdict of shape: {date: [{user: float(score)}, {...}]

    scores_dict = defaultdict(list)

    for entrydict in li_wellbeing_entries:

        entry_text = entrydict['text'].split(" ")  # entry_text = ['9.5\r\n\r\n--', '\r\nSignature', 'Signature\r\n']

        score = entry_text[0].split("\r")
        score = float(score[0])

        append_dict = {entrydict['user']: score}

        scores_dict[entrydict['date']].append(append_dict)

    # Scores_dict structures as following:
    # defaultdict(<class 'list'>{
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
    #           })

    return scores_dict


####################################################################
# Get the entries from database:
entries = get_db_entries()

# Change the date from str to datetime object:
change_date_format(entries)

# Change shape of the data to have usable format:
scores = get_scores(entries)

scores = dict(scores)  # change defaultdict to dict


#continue here

# Plot the stuff here
#simple_li = []
#for key,value in scores.items():
#
#    for item in value:
#
#        for k,v in item.items():
#            simple_li.append(v)
#
#print(simple_li)
#
#plt.plot(simple_li)
#plt.show()

print(scores)
# {datetime.date(2021, 4, 14): [
#                               {'M': 8.0},
#                               {'M': 8.0},
#                               {'T': 9.5}
#                              ],
#  datetime.date(2021, 4, 15): [
#                               {'M': 7.5},
#                               {'M': 4.5},
#                               {'M': 3.0},
#                               {'M': 6.0},
#                               {'M': 2.5},
#                               {'T': 6.5}
#                              ],
#  datetime.date(2021, 4, 16): [
#                               {'M': 6.5}
#                              ]
#  }


# Create Pandas DataFrame:
# TODO: work on this, it rewrite the score for user (put only one per user)
new_dict = {k: {k: v for userdict in li for k, v in userdict.items()} for k, li in scores.items()}

print(new_dict)

scores_df = pd.DataFrame.from_dict(new_dict, orient='index')

print(scores_df)
#

##index_df =
#score_df = pd.DataFrame.from_dict(scores)#, orient='index')#, orient=scores.keys())
##score_df = pd.Series(scores).apply(pd.Series).T
#print(score_df)
#
#
#def parse_dict_scores(dict_scores):
#    return_dict = defaultdict(list) #{}
#
#    for user in dict_scores:
#        #append_dict = {
#        #                'user': user,
#        #                'score': dict_scores[user]['score']
#        #}
#
#        append_dict = {user: dict_scores[user]['score']}
#
#        return_dict[dict_scores[user]['date']].append(append_dict)
#    return return_dict
#
#
#parsed_scores = parse_dict_scores(scores)
##print(parsed_scores)
##print(pd.DataFrame.from_records(parsed_scores))
#
#print(f"this is the parsed_dict_scores: {parsed_scores} ***************")
#
#dates = []
#frames = []
#
#for date, listuserscore in parsed_scores.items():
#    dates.append(date)
#    print(dates)
#    for userscore in listuserscore:
#        print(userscore)
#        print(type(userscore))
#        mini_df = pd.DataFrame(userscore, index=[0])
#        print(mini_df)
#        frames.append(mini_df)
#        print(frames)
#
#        #frames.append(pd.DataFrame(userscore, index=[0]))#, index=userscore))#, index=userscore.keys()))
#
#        #frames.append(pd.DataFrame(userscore))#, index=userscore))#, orient='index'))
#
#
#dataf = pd.concat(frames, keys=dates)
#
#print("*************************************")
#print(dataf)
#
#
##parsed_score_df = pd.DataFrame.from_dict({(i,j): parsed_scores[i][j] for i in parsed_scores.keys() for j in parsed_scores[i].keys()}, orien='index')
#
#
##parsed_score_df = pd.DataFrame.from_dict(parse_dict_scores(scores))

#
# Plot DataFrame:
plt.plot(scores_df)
plt.show()
