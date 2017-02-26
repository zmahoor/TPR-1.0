import pymysql.cursors
import pymysql
from time import gmtime, strftime

class DATABASE:

    def __init__(self):

        self.connection = pymysql.connect(host='96.126.111.207', user='root', \
            password='TwitchPlaysRobotics', db='TwitchPlays')

        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()

        print ("Database version : %s " % data)


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

        sql = "INSERT INTO commands VALUES('%d', '%s', '%d', '%s', '%d')" %(rowID, txt, num, currentTime, id)


        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("unable to insert data")
            self.connection.rollback()