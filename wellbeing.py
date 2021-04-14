from abstractions.database import get_db_entries

def get_scores(entries):
    scores = {}
    for entry in entries:
        if entry['subject'] == 'Wellbeing':
            entry_text = entry['text'].split(" ")
            #entry_text = entry['text'].split('')
            print(entry_text)#['text'])
            score = entry_text[0].split("\r")
            score = float(score[0])
            print(score)
            print(type(score))
            #TODO: need the sender!
            scores[entry['user']] = {'date': entry['date'], 'score': score}
            print(scores)
            #print(len(entry_text[0]))
            #scores[entry['key']] = {'score': entry['text'], 'date': entry['date']}
    return scores


entries = get_db_entries()
get_scores(entries)
