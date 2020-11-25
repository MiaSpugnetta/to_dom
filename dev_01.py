from imap_tools import MailBox, AND
import json
from collections import defaultdict
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from simple_colors import *
from deta import Deta


# Function to import parameters from external json file
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config


config = get_config('config.json')  # Get sensitive data stored in separate file

password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']
project_key = config['project_key']

# Access email account
mailbox = MailBox(imap_server)
mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg


# Initialize with a Project Key
deta = Deta(project_key)

# This connects to (or creates) a database
db = deta.Base("test_emails_db")


# If False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable useful for debug
use_stale = False

if use_stale:  # (is True):
    msg_dict = {
                    '4': {
                            'subject': 'TEST',
                            'text': '-- \r\nThomas Rost\r\n'
                         },
                    '5': {
                            'subject': 'Test',
                            'text': 'This is a test.\r\n'
                         },
                    '6': {
                            'subject': 'Test 2',
                            'text': 'Mia is my favorite\r\n'
                         }
               }
else:
    msg_dict = {}
    for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
        if msg.from_ in email_list:  # If message from email addresses in the   email list
            msg_dict[msg.uid] = {
                            'subject': msg.subject,
                            'text': msg.text
                                }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.
            mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder
            #db.put(msg)
# Prints number of email to the terminal
print(f"There are {len(msg_dict)} messages")


# Function to parse the dictionary. ???
def parse_dict(msg_dict):
    assert type(msg_dict) == dict, f"dummy you're using a {type(msg_dict)}"  # Make sure that the dictionary containing the emails is indeed a dictionary.

    return_dict = defaultdict(list)  # If a key is not found in the dictionary, a new entry (of type list)# Prints number of email to the terminal is created.

    for id in msg_dict:  # For message in the dictionary:
        append_dict = {  # Create dictionary that contains
                    'id': id,  # Number that identify the email (id=1 for first email, increases regularly, by one - duh). Basically an index.
                    'text': msg_dict[id]['text']  # Object+body of the email at said index (id).
        }

        return_dict[msg_dict[id]['subject'].capitalize()].append(append_dict)  # TODO: understand what kind of magic happens here. Additionally all subject are capitalised.
    #print(return_dict)
    #print("####################")
    ##print(append_dict)

    # {TODO: find a way to replace "ressource" with "resource"
        #new_dict = defaultdict()
        ##replace = "Ressource"
        ##replace_with = "Resource"
        #new_dict = {i:j for i,j in return_dict.items() if i != "Ressource"}
        #new_dict["Resource"] = return_dict["Ressource"]

        #return_dict['Resource'] = return_dict.pop('Ressource')
        #return_dict['subject'] = "Resource"
        #}

    return return_dict  # Returns a dictionary of dictionaries where the key is the subject (category) of the email and the value is a list of dictionaries that have that category as subject. Each of these subdictionary seems to have id and text as key-value pairs.

##################
#return_dict = parse_dict(msg_dict)
print(msg_dict)
subjects = []
#for i,d in msg_dict.items():
#    for subject in d:
#        subjects.append(d['subject'].capitalize())
#print(subjects)
print("******************")
stale_dict = {'9': {'subject': 'Idea', 'text': 'Meme preference predictor to minimize time spent looking for lulz\r\n'}, '11': {'subject': 'Idea', 'text': "1. Make a website (aixperiment.eu -> have the URL already)\r\n2. Put on it a showcase for thompson sampling\r\n3. First one is 'yhis headline gets people to click , this one doesn't) or\r\nsomething - build an experiment on the page!\r\n4. Add a housing predictor contextual thompson sampler - the Aigent?\r\n5. Offer to build things for people and offer an API\r\n"}, '12': {'subject': 'Feature request', 'text': 'Follow up on ideas - via website? Could refine things\r\n'}, '13': {'subject': 'Idea refinement', 'text': 'Aixperiment:\r\nAdd seo optimization tool as use case\r\nAdd adaptive pricing to use cases\r\n'}, '14': {'subject': 'Research cobeau', 'text': "Cobeau\r\n\r\nHow does the Models predictive uncertainty predict it's error\r\n\r\nMeasure on predictive mean variance! Not: estimate of true data\r\ndistribution - the scale is not there, not the same as NLPD!(ToDo: Write to\r\nMaurits about this!)\r\n\r\n\r\nMain thing to show:\r\n1. Does the Models uncertainty happen in the right spot during training?\r\n2. Did the model learn everything it can (cobeau goes down)\r\n3. Nonlinear: is the model too simple (i.e. can a more complex model make a\r\nconnection between error, uncertainty and input? This points towards not\r\nenough dof (why!)\r\n\r\n\r\nFrequentist:\r\nPearson's R\r\n\r\nBayesian: bayesian linear regression\r\nP(e_i|/sigma_i)\r\n\r\nAlso:\r\nP(e_i|/sigma_i, x_i) with nonlinear model\r\n"}, '15': {'subject': 'Idea', 'text': 'Habitica Integration\r\n'}, '16': {'subject': 'Task', 'text': 'Write Angela about bed\r\n'}, '17': {'subject': 'Task', 'text': 'Track food for Mia\r\n'}, '18': {'subject': 'Feature prior high', 'text': 'Forward emails to this address, get reminded of which ones need to be\r\nanswered\r\n'}, '19': {'subject': 'Ressource', 'text': 'http://shivanandroy.com/transformers-generating-arxiv-papers-title-from-abstracts/\r\n'}, '20': {'subject': 'Task', 'text': '1. Basic NLP Problem Like sent in here\r\n2. Upload to scailable?\r\n3. Make available via germanAI.de\r\n'}, '21': {'subject': 'Ressource', 'text': 'https://towardsdatascience.com/calculus-of-variations-demystified-4c822bb7fc23\r\n'}, '22': {'subject': 'resource', 'text': 'https://bair.berkeley.edu/blog/2019/02/15/false-discoveries/\r\n'}, '23': {'subject': 'task', 'text': 'prepare Cobeau presentation for LAB on the 3rd of november\r\n\r\n-- \r\nThomas Rost\r\n'}, '24': {'subject': 'Task', 'text': 'Write to Carlos\r\n'}, '38': {'subject': 'Task', 'text': "Build 'simulate your own Experiment'\r\n"}, '67': {'subject': 'Idea', 'text': 'Scicrum science driven scrum (exploration via TS)\r\n'}, '68': {'subject': 'Idea', 'text': 'Let your team bet on experiment outcomes to get the prior for aixperiment\r\n'}, '69': {'subject': 'Ressource !', 'text': 'https://nanonets.com/blog/key-value-pair-extraction-from-documents-using-ocr-and-deep-learning/\r\n'}, '70': {'subject': 'Ressource', 'text': 'https://github.com/google-research/multilingual-t5\r\n'}, '71': {'subject': 'Ressource pdf', 'text': '\r\n'}, '72': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/sciences/comments/jgqhml/the_temporal_association_of_introducing_and/\r\n'}, '73': {'subject': 'Attachment', 'text': 'Scale label 1\r\n'}, '74': {'subject': 'Attachment', 'text': 'Scale label 2\r\n'}, '75': {'subject': 'Taak', 'text': 'Add this and link to habitica\r\n\r\n\r\nhttps://chrome.google.com/webstore/detail/habitica-pomodoro-sitekee/iaanigfbldakklgdfcnbjonbehpbpecl?hl=en\r\n'}, '76': {'subject': 'Task', 'text': 'Make the Christmas picture for everyone and print them so they arrive in\r\ntime\r\n'}, '77': {'subject': 'Resource', 'text': 'https://towardsdatascience.com/introduction-to-bayesian-linear-regression-e66e60791ea7\r\n'}, '78': {'subject': 'Task', 'text': 'Write to Hazel about blue whales etc in uk and connections\r\n'}, '80': {'subject': 'Task', 'text': 'Social security set up\r\n\r\nFind out autonomo online stuff\r\n'}, '81': {'subject': 'Task', 'text': 'Follow up internet autonomo vs sl\r\n'}, '82': {'subject': 'Task', 'text': 'Write thompson sampler for Mia ibu vs aspirin vs paracetamol\r\n'}, '83': {'subject': 'Stories', 'text': "Werewolves on the moon\r\n\r\nIn 1969 during the first space walk people realize that every human is\r\nactually a werewolf, it's just that the thick atmosphere in combination\r\nwith earth's magnetic field keeps away the Lupine radiation\r\n"}, '84': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/MachineLearning/comments/josj1h/p_list_of_gan_and_deepfake_papers_and_github_repos/\r\n'}, '85': {'subject': 'Ressource', 'text': 'https://www.strio.co/blog/authentication-guide-with-fastapi/\r\n'}, '86': {'subject': 'Ressource', 'text': 'https://towardsdatascience.com/build-and-host-fast-data-science-applications-using-fastapi-823be8a1d6a0\r\n\r\n\r\n\r\n\r\nhttps://medium.com/@gabbyprecious2000/creating-a-crud-app-with-fastapi-part-one-7c049292ad37\r\n'}, '87': {'subject': 'Pong Game Tutorial — Kivy 1.11.1 documentation', 'text': 'https://kivy.org/doc/stable/tutorials/pong.html\r\n'}, '88': {'subject': 'Ressource', 'text': 'https://testdriven.io/blog/fastapi-mongo/\r\n-- \r\nThomas Rost\r\n'}, '89': {'subject': 'ressource', 'text': 'https://medium.com/@8B_EC/tutorial-serving-machine-learning-models-with-fastapi-in-python-c1a27319c459\r\n\r\n-- \r\nThomas Rost\r\n'}, '90': {'subject': 'Ressource', 'text': 'https://github.com/happilyeverafter95/iris-classifier-fastapi/blob/master/iris/router/iris_classifier_router.py\r\n'}, '91': {'subject': 'Ressource', 'text': 'https://www.docracy.com/1/generic-nda\r\n'}, '92': {'subject': 'Ressource', 'text': 'https://nondisclosureagreement.com/mutual.html\r\n'}, '93': {'subject': 'Ressource', 'text': 'https://www.fudzilla.com/news/51812-south-park-creators-turn-to-deep-fakes\r\n'}, '94': {'subject': 'task', 'text': 'add to the experimentation stuff:\r\n\r\nFragen:\r\n\r\n   1. ist es personalisierung (i.e. optimierung auf user level, Beispiel\r\n   Frage: funktioniert fuer Markus der FADM recommender besser oder der IC\r\n   recommender) oder globale optimierung (i.e. optimierung auf firmenlevel,\r\n   Beispiel Frage: bringt FASTAPI einen gewinn ueber FLASK; oder wird ein\r\n   gruener Button auf dieser Spezifischen Page eher geklickt als ein Blauer)\r\n   -> die Frage ist quasi: Wo sind wir spezifisch, beim user oder bei der\r\n   intervention\r\n   2. wenn global: Wie teuer ist es, wenn der User in der falschen Gruppe\r\n   bleibt? Teuer -> reassignment scheme (vielleicht sogar aktiv:\r\n   user/settings/switch button color?) Nicht teuer: assign-and-forget\r\n\r\n\r\n-- \r\nThomas Rost\r\n'}, '95': {'subject': 'ressource', 'text': 'https://github.com/Kludex/awesome-fastapi-projects\r\n\r\n-- \r\nThomas Rost\r\n'}, '96': {'subject': 'ressources', 'text': 'https://course.fast.ai/\r\n\r\n-- \r\nThomas Rost\r\n'}, '97': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/MachineLearning/comments/jtomhw/r_stanford_ai_lab_blog_bootleg_chasing_the_tail/\r\n'}, '98': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/learnmachinelearning/comments/judi83/3d_photo_inpainting_ai_brings_2d_illustrations_to/\r\n'}, '99': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/PhysicsPapers/comments/jt5bey/most_important_papers_in_the_last_20_years/\r\n'}, '100': {'subject': 'Ressource', 'text': 'https://lionbridge.ai/articles/three-types-of-deepfake-detection/\r\n'}, '101': {'subject': 'Stories', 'text': "Waiting for godbot\r\n\r\nStory of a couple or two couples who used to smoke and drink and party who\r\nkind of stopped doing any of that because they have a real shot at seeing\r\nactual AI come to pass and want to be healthy enough to enjoy that,\r\nwhatever it means.\r\n\r\nThey just finished watching a movie and are a bit tipsy and start talking\r\nabout how they used to live their lives and how they miss getting wasted\r\nand how the biggest self destruction that's left is eating cheese as\r\nlactose intolerant people. They also report how they understand that it's\r\ntrading in moments of bliss for eternity.\r\nIn the end either someone breaks into their flat and kills them or they\r\njust literally are left alone doing ths dishes and waiting for godot style\r\nthe audience realizes that godbot is not going to come\r\n"}, '102': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/MachineLearning/comments/jxnc2p/p_how_i_built_and_deployed_a_fun_serverless/\r\n'}, '103': {'subject': 'karpathy/minGPT: A minimal PyTorch re-implementation of the OpenAI\r\n GPT (Generative Pretrained Transformer) training', 'text': 'https://github.com/karpathy/minGPT\r\n'}, '104': {'subject': 'The Annotated Transformer', 'text': 'http://nlp.seas.harvard.edu//2018/04/03/attention.html\r\n'}, '105': {'subject': 'Code', 'text': 'http://nlp.seas.harvard.edu//code/\r\n'}, '106': {'subject': 'Ressource', 'text': 'https://ai.googleblog.com/2020/11/the-language-interpretability-tool-lit.html?m=1\r\n'}, '107': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/learnmachinelearning/comments/jxxlba/notebook_demonstrating_zeroshot_classification/\r\n'}, '108': {'subject': 'Explore the Moon with LUVMI-X – LUVMI-X', 'text': 'https://www.h2020-luvmi-x.eu/explore-the-moon-with-luvmi-x/\r\n'}, '109': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/deeplearning/comments/jxqibk/evaluation_of_text_generation_a_survey/\r\n'}, '110': {'subject': 'Ressource', 'text': 'https://jina.ai/\r\n'}, '111': {'subject': 'Ressource', 'text': 'https://www.reddit.com/r/MachineLearning/comments/jxrg9m/d_state_of_deepfakes_2020/\r\n'}, '112': {'subject': 'Ressource', 'text': 'https://github.com/graykode/ai-docstring\r\n'}, '113': {'subject': 'Ressource', 'text': 'https://rubikscode.net/2020/11/23/deploying-machine-learning-models-with-fastapi-and-angular/\r\n'}, '114': {'subject': 'ressource', 'text': 'https://towardsdatascience.com/how-to-build-and-deploy-a-machine-learning-model-with-fastapi-64c505213857\r\n\r\n-- \r\nThomas Rost\r\n'}}

dict_of_msgs = msg_dict.copy()
for i,j in dict_of_msgs.items():
    for subject in j:
        j['subject'].replace(j['subject'], j['subject'].capitalize())
        j['subject']
        subjects.append(j['subject'])
print(subjects)
print("#############")
#{i:j for i,j.capitalize() in msg_dict.items()}
print(dict_of_msgs)
#dict_of_msgs = msg_dict[id]['subject'].capitalize()
#print(msg_dict)
#for id, msg in msg_dict.items():
#    db.put(msg, key=str(id))


stories = db.fetch({'subject':'Stories'})
print(list(stories))

#after this everything is commented out, remove at the end of db attempt
## Function that composes the body of the email to send
#def generate_message(parsed_dict):
#    return_string = ''
#    #{ TODO: format text in email (i.e. categories in bold)
#    #start = "\033[1m"
#    #end = "\033[0;0m" #}
#    for subject in parsed_dict:  # For category in the dictionary:
#        return_string += f"{subject}, number of mails: {len(parsed_dict[subject])}:\n\n"  # Append the name of the category and the number of messages that belong to that category.
#
#        for content in parsed_dict[subject]:  # For each subdictionary:
#            return_string += f"{content['id']}: {content['text']}\n"  # Append the id number (so to have a kind of chronological order) and the actual body to the message in the making.
#
#        return_string += '_________________________\n\n\n'  # Add a separator after each category.
#
#    return return_string  # Return composed message
#
#
## Create parsed dictionary
#return_dict = parse_dict(msg_dict)
#
############################################
## Create email to be sent
#
#context = ssl.create_default_context()  # Create a secure SSL context
#
#port = config['port']
#smtp_server = config['smtp_server']
#sender_email = config['sender_email']
#receiver_email = config['receiver_email']
#
#message = MIMEMultipart()
#message["Subject"] = "Daily report"
#
#body_email_dict = parse_dict(msg_dict)
#body_email = generate_message(body_email_dict)
#first_crap = MIMEText(body_email)
#message.attach(first_crap)
#
#
## Send composed email
#with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:  # Makes sure that the connection is automatically closed at the end of the indented code block. If port is 0 or not specified, standard port for SMTP over SSL is 465.
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message.as_string())
#

# Log out from the email account
mailbox.logout()
