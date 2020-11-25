from deta import Deta
deta = Deta('a0x1dprr_AuyJDDRuHFy772BTVZN8mhTkYDta82bM')
db = deta.Base('simpleDB')

user1 = {
    "key": "Mia",
    "likes": "Thomas",
    "hometown": "Rome"
}

user2 = {
    "key": "Thomas",
    "likes": "Mia, at least I hope",
    "hometown": "Munich"

}

user4 = {
    "name": "John",
    "likes": "whiskey",
    "hometown": "Rome",
}

db.put(user1)
db.put(user2)
db.put(user1)
user3 = db.get("Thomas")
assert user3 == user2, 'not same thomas!'

john_whiskey = db.put(user4)
#user_x = db.get("42")
#print(john_whiskey)

mias = db.fetch({'likes':'Thomas'})
#print(list(mias))


#num_users = 0
#for user in db.fetch():
#    num_users += 1
#
#
#print(num_users)
#key_list = []
#for user in db.fetch():
#    for user_dict in user:
#        key_list.append(user_dict['key'])
#print(key_list)

user = db.fetch()[0]
for user_dict in user:
    key_list.append(user_dict['key'])
print(key_list)

for user in db.fetch():
    for user_dict in user:
        if user_dict['key'] in key_list:
            db.delete(user_dict['key'])

user == [[ {}.{}, {}]][0] ==
 [{}, ]