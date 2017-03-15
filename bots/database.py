import pymysql.cursors
import pymysql
from time import gmtime, strftime
from settings import *

class DATABASE:

    def __init__(self):

        self.connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASS, db=MYSQL_DB)

        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()

        print ("Database version : %s " % data)
    
    def Add_User(self, username, time):

        sql = "INSERT INTO users(userName, timeAdded, numChats) VALUES('%s', '%s', 1)\
            ON DUPLICATE KEY UPDATE numChats = numChats + 1;"%(username, time)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to update table users")

    def Add_User_Parent(self, user, parent):

        sql = "UPDATE users set parentName='%s' WHERE userName='%s';"%(parent, user)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not update the parent")
            self.connection.rollback()

    def Add_Reinforcement(self, color, reward):
        # if the startTime is beyond n minutes then discard this reward
        if reward == 'y':
            sql = " UPDATE display set numYes=numYes+1 WHERE color='%s'\
             ORDER BY startTime DESC LIMIT 1;"%(color)
        elif reward == 'n':
            sql = " UPDATE display set numNo=numNo+1 WHERE color='%s'\
             ORDER BY startTime DESC LIMIT 1;"%(color)
        else: return

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not insert the reinforcement")
            self.connection.rollback()

    def Add_Command(self, command, color, time):

        # print(command, color, time)
        sql = "INSERT INTO command_log(cmdTxt, color, timeArrival) VALUES('%s', '%s', '%s');"%(command, color, time)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to log this command")

        sql = "INSERT INTO unique_commands(cmdTxt, timeAdded, numIssued) VALUES('%s', '%s', 1)\
            ON DUPLICATE KEY UPDATE numIssued = numIssued + 1;"%(command, time)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to add this new command")

    def Fetch_New_Chat(self):
        result = None
        try:
            #find the oldest piece of unprocessed chat
            sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            chatID = result[0]

            print(result)

            #modify the row as processed
            sql = "UPDATE chats SET processed=1 WHERE chatID='%d';"%(chatID)
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            # print("no new chat message is found")
            self.connection.rollback()

        return result

    def Fetch_New_Color(self):
        color = ""
        try:
            sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            chatID = result[0]
            color = result[3]

            print(result)
            sql = "UPDATE chats SET processed=1 WHERE id='%d';"%(chatid)
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            print("please paint me with blue|red|green|white|black|purple|cyan|yellow")
            self.connection.rollback()

        return color

    def Insert_Chat(self, username, current_time, msg):
        #INSERT INTO chats VALUES (ID, time, user, txt);
        sql = "INSERT INTO chats(timeArrival, username, txt) VALUES('%s', '%s', '%s');"\
        %(current_time, username, msg)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            # print("successfull insert")
        except:
            print("unable to insert data")
            self.connection.rollback()
                
        # self.connection.close()          

    def Fetch_A_Command(self, id):

        commTxt = ""
        try:
            # find the most recent command for the current robot id, 
            # assuming only the most popular command during each interval is inserted in this table
            
            sql = "SELECT * FROM commands WHERE robotID ='%d' ORDER BY timeA DESC LIMIT 1;" %(id)
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            commTxt = result[1]
            print(result)
            print("ISSUED COMMAND: %s"%commTxt)

        except:
            print("unable to fetch data")
            self.connection.rollback()

        # self.connection.close()
        return(commTxt)

    def Insert_A_Command(self):

        # sql = "INSERT INTO users VALUES('%d', '%s', '%d', '%d')" %(1001, 'lingling', 11, 11)

        rowID = 1005
        txt = 'dance'
        num = 1
        robotID = 2
        currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        sql = "INSERT INTO commands VALUES('%d', '%s', '%d', '%s', '%d');" %(rowID, txt, num, currentTime, id)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("unable to insert data")
            self.connection.rollback()