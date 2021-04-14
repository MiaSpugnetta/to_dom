from abstractions.database import get_db_entries
from _datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from collections import defaultdict


# Function to convert the date string to type datetime object
def change_date_format(entries):
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            entry['date'] = datetime.strptime(entry['date'], '%a, %d %b %Y %H:%M:%S %z').date()
            print(entry['date'])
            print("*******")
    return entries

    #return updated_entries


def get_scores(entries):
    scores = {}
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            entry_text = entry['text'].split(" ")
            #print(entry_text)
            score = entry_text[0].split("\r")
            score = float(score[0])
            #print(score)
            scores[entry['user']] = {'date': entry['date'], 'score': score}
    #print(scores)
            #print(len(entry_text[0]))
            #scores[entry['key']] = {'score': entry['text'], 'date': entry['date']}
    return scores


entries = get_db_entries()
change_date_format(entries)

scores = get_scores(entries)
print(scores)
print(scores.keys())
print("&&&&&&&&&&&&&")
print(type(scores['T']['date']))
print((scores['T']['date']))


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

print(f"this is the parsed_dict_scores: {parsed_scores}")

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

