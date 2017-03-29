import pymysql.cursors
import pymysql
from time import *
from settings import *

class DATABASE:

    def __init__(self):

        self.connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASS, db=MYSQL_DB)

        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()

        print ("Database version : %s " % data)
    
    def Insert_Chat(self, username, current_time, msg):
        #INSERT INTO chats VALUES (ID, time, user, txt);
        sql = """INSERT INTO chats(timeArrival, username, txt) VALUES
        ('%s', '%s', '%s');"""%(current_time, username, msg)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            # print("successfull insert")
        except:
            print("unable to insert data")
            self.connection.rollback()
    
    def Add_To_Help(self, user, txt, time):
        sql = """INSERT IGNORE INTO helps(txt, userName, timeArrival) VALUES('%s', '%s');"""%(user, txt, time)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert help request")

    def Add_User(self, username, time):
        sql = """INSERT IGNORE INTO users(userName, timeAdded) VALUES('%s', '%s');"""%(username, time)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert new user")

    def Add_User_Parent(self, user, parent):
        sql = "UPDATE users set parentName='%s' WHERE userName='%s';"%(parent, user)
        print
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not update the parent")
            self.connection.rollback()

    def Add_Reward_To_Display(self, color, reward, arrivalTime):
        # if the startTime is beyond 3 minutes, discard this reward
        
        if reward == 'y':
            sql = """ UPDATE display set numYes=numYes+1 WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE display set numNo=numNo+1 WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'l':
            sql = """ UPDATE display set numLike=numLike+1 WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE display set numDislike=numDislike+1 WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        else: return

        try:
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not insert the reinforcement")
            self.connection.rollback()

    def Add_To_RewardLog(self, username, color, reward, time):
        sql = """INSERT INTO reward_log(userName, reward, color, timeArrival) VALUES
        ('%s', '%s', '%s', '%s');"""%(username, reward, color, time)

        try:
            print
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to log this reward")

    def Update_Total_Fitness(self, color, reward, arrivalTime):
        if reward == 'y':
            sql = """ UPDATE robots set totalFitness=totalFitness+1 WHERE 
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE robots set totalFitness=totalFitness-1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        else: return

        try:
            print
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not update the robot's fittness")
            self.connection.rollback()

    def Update_Total_Likeability(self, color, reward, arrivalTime):
        if reward == 'l':
            sql = """ UPDATE robots set totalLikeability=totalLikeability+1 WHERE 
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE robots set totalLikeability=totalLikeability-1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and timediff('%s', startTime) < '00:03:00'
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        else: return

        try:
            print
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not update the robot's fittness")
            self.connection.rollback()

    # def Fetch_Total_Fitness(self, robotID):
    #     sql = """SELECT SUM(numYes) FROM display
    #     WHERE robotID='%d';"""%(robotID)

    #     try:
    #         self.cursor.execute(sql)
    #         self.connection.fetchone()
    #     except:
    #         print("could not upadate the fittness")
    #         self.connection.rollback()

    def Add_To_CommandLog(self, username, command, time):
        sql = """INSERT INTO command_log(userName, cmdTxt, timeArrival) VALUES
        ('%s', '%s', '%s');"""%(username, command, time)

        try:
            print
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to log this command")

    def Add_Command(self, command, time):
        sql = """INSERT INTO unique_commands(cmdTxt, timeAdded, numIssued) VALUES('%s', '%s', 1)
            ON DUPLICATE KEY UPDATE numIssued = numIssued + 1;"""%(command, time)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to add this new command")

    def Add_Robot(self, robotType):
        robotID = 0
        sql = "INSERT INTO robots(type) VALUES('%s');"%(robotType)

        try:
            self.cursor.execute(sql)
            robotID = self.connection.insert_id()
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert the robot")

        return robotID

    def Add_Command_To_Display(self, robotID, cmdTxt, color, startTime):
        sql = """INSERT INTO display(robotID, cmdTxt, color, startTime) VALUES
        ('%d','%s','%s', '%s');"""%(robotID, cmdTxt, color, startTime)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert the robot into the display")

    def Update_Robot_Evaluation(self, robotID):
        sql = "UPDATE robots SET numEvals=numEvals+1 WHERE robotID='%d';"%(robotID)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            # print("no new chat message is found")

    def Update_Scores(self, user):
        sql= """UPDATE users SET score=(SELECT count(*) FROM chats WHERE
         userName = '%s') WHERE userName = '%s' ;"""%(user, user)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()

    def Kill_Robot(self, robotID):
        #update the robot with dead flag as 1--kill it--
        sql = "UPDATE robots set dead=1 WHERE robotID='%d';"%(robotID)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to kill the robot")

    def Fetch_User_Score(self, user):
        sql = "SELECT * FROM users WHERE userName='%s';"%(user)
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:
            print("unable to retrieve user's score")

        return result

    def Fetch_Top_Users(self, topn):
        sql = """SELECT userName, score FROM users ORDER BY score DESC LIMIT %d;"""%(topn)
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            print("unable to retrieve score table")

        return result

    def Fetch_Alive_Robots(self, robotType):
        #find all the robots with the dead flag as zero --alive--
        sql = "SELECT * FROM robots WHERE dead=0 and type='%s';"%(robotType)
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            print("unable to retrieve alive robots")

        return result

    def Fetch_New_Chat(self):
        #find the oldest piece of unprocessed chat
        sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
        result = None
        chatID = 0
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            chatID = result['chatID']
        except:
            pass
            # print(result)

        #update the processed flag as 1 for that piece of chat
        sql = "UPDATE chats SET processed=1 WHERE chatID='%d';"%(chatID)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            # print("no new chat message is found")

        return result

    def Fetch_New_Color(self):
        color = ""
        try:
            sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            chatID = result['chatID']
            color = result['txt']

            print(result)
            sql = "UPDATE chats SET processed=1 WHERE chatID='%d';"%(chatID)
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            print("please paint me with blue|red|green|white|black|purple|cyan|yellow")

        return color

    def Fetch_All_Commands(self, topn):
        sql = """SELECT cmdTxt, numIssued from unique_commands ORDER BY numIssued DESC LIMIT %d;"""%(topn)

        result = None
        try:            
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            # print result
        except:
            print("unable fetching all the unique commands")

        return result

    def Fetch_Popular_Command(self):
        #find the most popular command where processed=0
        sql = """SELECT count(cmdLogID) as cmdCount, cmdTxt FROM command_log WHERE 
        processed =0 GROUP BY cmdTxt ORDER BY COUNT(cmdLogID) DESC LIMIT 1;"""

        result = None
        try:            
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            # print result
        except:
            pass

        #change those commands as processed=1
        sql = """ UPDATE command_log SET processed=1 WHERE processed =0;"""
        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            self.connection.rollback()
            print("unable to fetch a command")

        if result == None: 
            return({'cmdCount':0, 'cmdTxt':"stay still"})
        
        return result
