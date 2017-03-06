import string
import pymysql
import datetime, time
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom

def createTable(tableName, databaseName):
    #create a table in a given database
    cur.execute('use ' + databaseName + ';')
    cur.execute('CREATE TABLE ' + tableName + ' (timeA CHAR(20), timeR CHAR(20), msg CHAR(100));')

def deleteTable(tableName, databaseName):
    #deletes a table in a given database
    cur.execute('use ' + databaseName + ';')
    cur.execute('DROP TABLE IF EXISTS ' + tableName + ';')
    print('done')
    
def bigRedButton():     #change to drop all?
    #stop everything, wipe database
    #use before editing datebase
    cur.execute('DROP DATABASE IF EXISTS TwitchPlays;')

def bigGreenButton():   #change to create all? (all databases necessary for data)
    #start everything
    #define database
    #cur.execute('CREATE DATABASE TwitchPlays;')
    #cur.execute('USE TwitchPlays;')
    cur.execute('CREATE TABLE reinforcements (ID INT(20), txt CHAR(10), timeA CHAR(30), timeR CHAR(30), robot INT(10));')
    cur.execute('CREATE TABLE robots (ID INT(20), numYes INT(10), numNo INT(10), cmd INT(10));')
    cur.execute('CREATE TABLE commands (ID INT(20), txt CHAR(20), num INT(10), timeA CHAR(30), robot INT(10));')
    cur.execute('CREATE TABLE users (ID INT(20), name CHAR(30), numChats INT(20), score INT(10));')
    cur.execute('CREATE TABLE chats (ID INT(20), timeA CHAR(30), user CHAR(30), txt CHAR(30));')



#connect to the database
conn = pymysql.connect(host="96.126.111.207",port=3306,user="root",passwd="TwitchPlaysRobotics",db="TwitchPlays")
cur = conn.cursor()
cur.execute('USE TwitchPlaysRobotics;')

print("Welcome to QueryBot!")
print("You can send MySQL queries to the TwitchPlaysRobotics database.")
print("To end querying, type 'exit()'")
print("For normal MySQL queries, type 'n'")
print("For simplified syntax, type 's'")
print("The mode can be toggled at any time")

help = 'QUERIES: \n\
        green_button   -- Create all tables \n\
        red_button     -- Drops the database **Caution** \n\
        delete [name]  -- Deletes the table of the given name'
        
    
user_input = ""
expert_mode = False


while (True):
    
    user_input = raw_input('QUERY: ')
    q = user_input.lower()
    
    if (q == 'exit()'):
        break
    elif (q == 'help'):
        print(help)
    elif (q == 'n'):
        expert_mode = True
        print('Commands will now be in standard MySQL syntax.')
        continue
    elif (q == 's'):
        expert_mode = False
        print("Commands will now be simplified. Type 'help' for options")

    if (expert_mode):
        try:
            cur.execute(user_input)
        except pymysql.ProgrammingError as e:
            print('There is an error in your MySQL syntax, please try again.')
            view = raw_input('View error message? (y/n)')
            if (view.lower() == 'y' or view.lower() == 'yes'):
                print(e)
            else:
                continue
    else:
        if (q == 'green_button'):
            bigGreenButton()
        elif (q == 'red_button'):
            check = raw_input('Are you sure you want to delete the database? (y/n) ')
            if (check.lower() == 'y' or check.lower() == 'yes'):
                bigRedButton()
            else:
                continue
        elif (q[0:6] == 'delete'):
            deleteTable(q[7:], 'TwitchPlaysRobotics')
            









