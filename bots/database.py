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

    def Fetch_New_Color(self):

        color = ""

        try:
            sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeA ASC LIMIT 1;"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            color = result[3]
            chatid = result[0]

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
        sql = "INSERT INTO chats(timeA, username, txt) VALUES('%s', '%s', '%s');"%(current_time, username, msg)
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