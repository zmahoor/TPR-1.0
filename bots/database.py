import pymysql.cursors
import pymysql
from time import *
import datetime
from settings import *
import sys

class DATABASE:

    def __init__(self):

        try:
            self.connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                password=MYSQL_PASS, db=MYSQL_DB)

            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("SELECT VERSION()")
            data = self.cursor.fetchone()
            print ("Database version : %s " % data)
        except:
            print "Unable to connect to database...check your internet connection or the settings"
            sys.exit()
    
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
        sql = """INSERT IGNORE INTO helps(txt, userName, timeArrival) 
        VALUES('%s','%s','%s');"""%(txt, user, time)

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
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE display set numNo=numNo+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'l':
            sql = """ UPDATE display set numLike=numLike+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE display set numDislike=numDislike+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        else: return

        try:
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print("could not insert the reward")
            self.connection.rollback()

    def Add_To_RewardLog(self, username, color, reward, time):
        sql = """INSERT INTO reward_log(userName, reward, color, timeArrival) VALUES
        ('%s', '%s', '%s', '%s');"""%(username, reward, color, time)

        try:
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
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE robots set totalFitness=totalFitness-1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        else: return

        try:
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
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE robots set totalLikeability=totalLikeability-1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        else: return

        try:
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

        startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")

        sql = """INSERT INTO display(robotID, cmdTxt, color, startTime) VALUES
        ('%d','%s','%s', '%s');"""%(robotID, cmdTxt, color, startTime)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert the robot into the display")

        sql = "UPDATE robots SET numEvals=numEvals+1 WHERE robotID='%d';"%(robotID)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            # print("no new chat message is found")

    def Update_Users_Score(self):

        sql= """SELECT * from users;"""

        results = None

        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            print "unable to fetch user names"

        if results == None: return

        for row in results:

            user = row['userName']

            print user

            sql= """UPDATE users SET score=(SELECT count(*) FROM reward_log WHERE
             userName = '%s') + (SELECT count(*) FROM command_log WHERE
             userName = '%s') WHERE userName = '%s' ;"""%(user, user, user)

            try:
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()

    def Update_Commands_Score(self):

        sql = """ SELECT cmdTxt, min(startTime) as firstTime, max(startTime) as lastTime
            from display group by cmdTxt;"""

        results = None
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            pass

        print len(results)

        if results == None: return

        for row in results:

            # print row

            command = row['cmdTxt']

            start_time = row['firstTime']

            last_time  = row['lastTime']

            first_sum = 0

            second_sum = 0

            mid_time = start_time + (last_time - start_time)/2

            # print mid_time

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as firstSum FROM 
                    display WHERE startTime <= '%s' and cmdTxt='%s';"""%(mid_time, command)

            results = None
            try:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
            except:
                pass

            # print results

            if results[0]['cmdTxt'] != None: 
                first_sum = results[0]['firstSum']

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as secondSum FROM
             display WHERE startTime > '%s' and cmdTxt='%s';"""%(mid_time, command)

            results = None
            try:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
            except:
                pass

            # print results

            if results[0]['cmdTxt'] != None: 
                second_sum = results[0]['secondSum']

            # print command ,first_sum-second_sum

            sql = """UPDATE unique_commands SET totalLearnability ='%f' WHERE 
                cmdTxt ='%s';"""%(first_sum - second_sum, command)

            try:
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                print "failed to update likeability"

            print

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

    #return a list of all commands along with their scores and ranks
    # that were typed (interval) seconds before the current time
    def Fetch_Recent_Typed_Command(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        sql = """SELECT uc.cmdTxt, uc.totalLearnability, cl.timeArrival, 
        FIND_IN_SET( uc.totalLearnability, (SELECT GROUP_CONCAT( uc.totalLearnability 
        ORDER BY uc.totalLearnability DESC )
        FROM unique_commands as uc )) AS rank
        FROM command_log as cl
        JOIN unique_commands as uc on cl.cmdTxt = uc.cmdTxt
        WHERE cl.timeArrival
        BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.connection.commit()
        except:
            print("unable to retrieve most recent typed command")

        return result


    def Fetch_Recent_Active_Users(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        print current_time, prev_time

        sql = """SELECT c.username, u.score, c.timeArrival, 
        FIND_IN_SET( u.score, (SELECT GROUP_CONCAT( u.score ORDER BY u.score DESC ) FROM users as u )) AS rank
        FROM chats as c 
        JOIN users as u on u.username = c.username
        WHERE c.timeArrival
        BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.connection.commit()
        except:
            print("unable to retrieve most recent active users")

        return result

    def Fetch_Alive_Robots(self, robotType):
        #find all the robots with the dead flag as zero --alive--
        sql = "SELECT * FROM robots WHERE dead=0 and type='%s';"%(robotType)
        result = list()
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

    def Fetch_Oldest_Help(self):
        result=None
        try:
            sql = "SELECT * FROM helps WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            helpID = result['helpID']

            print(result)
            sql = "UPDATE helps SET processed=1 WHERE helpID='%d';"%(helpID)
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            pass

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

    def Fetch_For_Command_Window(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        sql ="""SELECT userName, cmdTxt, timeArrival FROM command_log
        WHERE timeArrival BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        result = None
        try:            
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.connection.commit()
        except:
            print("unable fetching the most recent type command")

        return result

    def Fetch_Top_Commands(self, topn):
        sql = """SELECT cmdTxt as cmd, totalLearnability as score FROM unique_commands 
        ORDER BY score DESC LIMIT %d;"""%(topn)

        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            print("unable to retrieve command table")

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

        # if result == None: 
        #     return({'cmdCount':0, 'cmdTxt':"stay still"})
        
        return result


    def Set_Current_Command(self, currentCommand, prevCommand):

        sql= """ UPDATE unique_commands set active=1 WHERE cmdTxt='%s';"""%(currentCommand)

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            self.connection.rollback()
            print("unable to set the current command")

        sql= """UPDATE unique_commands set active=0 WHERE cmdTxt='%s';"""%(prevCommand)

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except:
            self.connection.rollback()
            print("unable to unset the previous command")



