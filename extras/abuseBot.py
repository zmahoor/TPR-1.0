import string
import pymysql
from database import DATABASE
from settings import *
import datetime

db = DATABASE()

users = db.fetch_for_abuse_bot()

if users is None:
    print 'No users to print...or something went wrong!' 

else:
    with open('./tmp/abuse.log','w') as f:
        for user in users:
            line = user['cmdTxt'] + '  ' + user['userName'] + '\n'
            f.write(line)

