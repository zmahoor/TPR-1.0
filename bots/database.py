import pymysql.cursors
import pymysql
from time import *
import datetime
from settings import *
import sys
import numpy as np

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
    
    def Execute_Update_Sql_Command(self, sql_command, err_msg=""):

        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
        except:
            print(err_msg)
            self.connection.rollback()

    def Execute_Select_Sql_Command(self, sql_command, err_msg=""):

        results = None
        try:
            self.cursor.execute(sql_command)
            results = self.cursor.fetchall()
            self.connection.commit()
        except:
            print(err_msg)
        return results

    def Execute_SelectOne_Sql_Command(self, sql_command, err_msg=""):

        results = None
        try:
            self.cursor.execute(sql_command)
            results = self.cursor.fetchone()
            self.connection.commit()
        except:
            print(err_msg)
        return results


    def Add_To_Chat_Table(self, username, current_time, msg):
        sql = """INSERT INTO chats(timeArrival, username, txt) VALUES
        ('%s', '%s', '%s');"""%(current_time, username, msg)

        err_msg = "Failed to insert the chat message..."
        self.Execute_Update_Sql_Command(sql, err_msg)
    
    def Add_To_Help_Table(self, user, txt, time):
        sql = """INSERT IGNORE INTO helps(txt, userName, timeArrival) 
        VALUES('%s','%s','%s');"""%(txt, user, time)

        err_msg = "Failed to insert help request.."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Add_To_User_Table(self, username, time):

        sql = """INSERT IGNORE INTO users(userName, timeAdded) VALUES('%s', '%s');"""%(username, time)
        err_msg = "Fialed to insert a new user..."
        self.Execute_Update_Sql_Command(sql, err_msg)
        
    def Add_Reward_To_Display_Table(self, color, reward, arrivalTime):
        # if the startTime is beyond 2 minutes, discard this reward
        
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

        err_msg = "Failed to insert the reward into the display table..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Add_To_RewardLog_Table(self, username, color, reward, time):
        sql = """INSERT INTO reward_log(userName, reward, color, timeArrival) VALUES
        ('%s', '%s', '%s', '%s');"""%(username, reward, color, time)

        err_msg = "Failed to log this reward..."

        self.Execute_Update_Sql_Command(sql, err_msg)

    def Add_To_CommandLog_Table(self, username, command, time):
        sql = """INSERT INTO command_log(userName, cmdTxt, timeArrival) VALUES
        ('%s', '%s', '%s');"""%(username, command, time)

        err_msg = "Failed to log this command..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Add_To_Unique_Commands_Table(self, command, time, wordToVec):

        sql = """INSERT IGNORE INTO unique_commands(cmdTxt, timeAdded, 
            wordToVec, totalLearnability, active) VALUES
            ('%s', '%s', '%f', 0, 0);"""%(command, time, wordToVec)

        err_msg = "Failed to add this new command..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Add_To_Robot_Table(self, robotType):
        robotID = 0
        sql = "INSERT INTO robots(type) VALUES('%s');"%(robotType)
        err_msg = "Failed to insert the robot into the robots table..."

        try:
            self.cursor.execute(sql)
            robotID = self.connection.insert_id()
            self.connection.commit()
        except:
            self.connection.rollback()
            print("unable to insert the robot")

        return robotID

    def Add_Command_To_Display_Table(self, robotID, cmdTxt, color, startTime):

        startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")

        sql = """INSERT INTO display(robotID, cmdTxt, color, startTime) VALUES
        ('%d','%s','%s', '%s');"""%(robotID, cmdTxt, color, startTime)

        err_msg = "Failed to insert a robot into the display table..."
        self.Execute_Update_Sql_Command(sql, err_msg)

        sql = "UPDATE robots SET numEvals=numEvals+1 WHERE robotID='%d';"%(robotID)
        err_msg = "Failed to update number of evaluations for a robot..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Update_User_Parent(self, user, parent):

        sql = """UPDATE users set parentName='%s' WHERE userName='%s' 
        and parentName is NULL;"""%(parent, user)
        err_msg = "Failed to update the user's parent..."
        self.Execute_Update_Sql_Command(sql, err_msg)

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

        err_msg = "Failed to update the robot's fittness..."
        self.Execute_Update_Sql_Command(sql, err_msg)

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

        err_msg = "Failed to update the robot's fittness..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Update_Users_Score(self):

        sql= """SELECT * from users;"""
        err_msg = "Failed to fetch all usernames..."
        records = self.Execute_Select_Sql_Command(sql, err_msg)

        if records == None: return

        for row in records:

            user = row['userName']
            # print user

            sql= """UPDATE users SET score=(SELECT count(*) FROM reward_log WHERE
             userName = '%s') + (SELECT count(*) FROM command_log WHERE
             userName = '%s') WHERE userName = '%s' ;"""%(user, user, user)
            
            err_msg = "Failed to update user's score..."
            self.Execute_Update_Sql_Command(sql, err_msg)

    def Update_Commands_Score(self):

        sql = """ SELECT cmdTxt, min(startTime) as firstTime, max(startTime) as lastTime
            from display group by cmdTxt;"""
        err_msg = "Faild to fetch command names..."
        records = self.Execute_Select_Sql_Command(sql, err_msg)

        if records == None: return

        for row in records:
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
            err_msg = "Faild to fetch command names"
            result = self.Execute_SelectOne_Sql_Command(sql, err_msg)

            # print result

            if result['cmdTxt'] != None: 
                first_sum = result['firstSum']

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as secondSum FROM
             display WHERE startTime > '%s' and cmdTxt='%s';"""%(mid_time, command)

            result = self.Execute_SelectOne_Sql_Command(sql)
            # print result

            if result['cmdTxt'] != None: 
                second_sum = result['secondSum']

            # print command ,first_sum-second_sum

            sql = """UPDATE unique_commands SET totalLearnability ='%f' WHERE 
                cmdTxt ='%s';"""%(first_sum - second_sum, command)

            err_msg = "Failed to update command's learnability"
            self.Execute_Update_Sql_Command(sql, err_msg)
    
    #update the robot with dead flag as 1--kill it--
    def Kill_Robot(self, robotID):
        sql = "UPDATE robots set dead=1 WHERE robotID='%d';"%(robotID)
        err_msg = "Failed to kill the robot..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Get_New_Word_Vector(self):

        sql="""SELECT wordToVec FROM unique_commands;"""
        err_msg = "unable to fetch user names"
        results = self.Execute_Select_Sql_Command(sql, err_msg)

        newIndex = 0
        if results != None:
            newIndex = np.random.random()

            while newIndex in results:
                newIndex = np.random.rand()
        else:
            newIndex = np.random.random()
        return newIndex

    def Fetch_From_Disply_Table(self, startTime):

        sql = """SELECT d.robotID, r.type, d.cmdTxt, u.wordToVec, 
         d.numYes, d.numNo, d.numLike, d.numDislike
         from display as d JOIN robots as r ON d.robotID=r.robotID 
         JOIN unique_commands as u on d.cmdTxt=u.cmdTxt
         WHERE d.startTime='%s';"""%(startTime)

        err_msg = "Failed to retrieve record of a dispaly..."
        return self.Execute_SelectOne_Sql_Command(sql, err_msg)

    def Fetch_User_Score(self, user):

        sql = "SELECT * FROM users WHERE userName='%s';"%(user)
        err_msg = "Failed to retrieve a user's score"
        return self.Execute_SelectOne_Sql_Command(sql, err_msg)

    def Fetch_Top_Users(self, topn):

        sql = """SELECT userName, score FROM users ORDER BY score DESC LIMIT %d;"""%(topn)
        err_msg = "Failed to retrieve scores of top users..."
        return self.Execute_Select_Sql_Command(sql, err_msg)

    #return a list of all commands along with their scores and ranks
    # that were typed (interval) seconds before the current time
    def Fetch_Recent_Typed_Command(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        sql = """SELECT uc.cmdTxt as cmd, uc.totalLearnability as score, cl.timeArrival, 
        FIND_IN_SET( uc.totalLearnability, (SELECT GROUP_CONCAT( uc.totalLearnability 
        ORDER BY uc.totalLearnability DESC )
        FROM unique_commands as uc )) AS rank
        FROM command_log as cl
        JOIN unique_commands as uc on cl.cmdTxt = uc.cmdTxt
        WHERE cl.timeArrival
        BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        err_msg = "Failed to retrieve the most recent typed command..."
        return self.Execute_Select_Sql_Command(sql, err_msg)

    def Fetch_Recent_Active_Users(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        print current_time, prev_time

        sql = """SELECT c.username as userName, u.score, c.timeArrival, 
        FIND_IN_SET( u.score, 
        (SELECT GROUP_CONCAT( u.score ORDER BY u.score DESC ) FROM users as u )) AS rank
        FROM chats as c 
        JOIN users as u on u.username = c.username
        WHERE c.timeArrival
        BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        err_msg = "Failed to retrieve the most recent active users..."
        return self.Execute_Select_Sql_Command(sql, err_msg)

    #find all the robots with the dead flag as zero --alive--
    def Fetch_Alive_Robots(self, robotType):

        sql = "SELECT * FROM robots WHERE dead=0 and type='%s';"%(robotType)
        err_msg = "Failed to retrieve alive robots..."
        return self.Execute_Select_Sql_Command(sql, err_msg)

    def Fetch_An_Unprocessed_Chat(self):
        #find the oldest piece of unprocessed chat
        sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
        result = self.Execute_SelectOne_Sql_Command(sql)

        if result != None:
            chatID = result['chatID']
            #update the processed flag as 1 for that piece of chat
            sql = "UPDATE chats SET processed=1 WHERE chatID='%d';"%(chatID)
            self.Execute_Update_Sql_Command(sql)

        return result

    def Fetch_Oldest_Help(self):

        sql = "SELECT * FROM helps WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
        err_msg = "Failed to fetch the oldest unprocessed help request..."
        result = self.Execute_SelectOne_Sql_Command(sql, err_msg)

        if result != None:
            helpID = result['helpID']
            sql = "UPDATE helps SET processed=1 WHERE helpID='%d';"%(helpID)
            self.Execute_Update_Sql_Command(sql, err_msg)

        return result
        
    def First_Time_Contributer(self, username):

        sql ="""SELECT userName FROM reward_log where userName='%s' union 
        SELECT userName FROM command_log where userName='%s';"""%(username, username)

        err_msg = "Failed to fetch information about this user..."
        result = self.Execute_Select_Sql_Command(sql, err_msg)

        if result == (): 
            return True
        
        return False

    def Fetch_For_Command_Window(self, interval=10):

        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        sql ="""SELECT userName, cmdTxt, timeArrival FROM command_log
        WHERE timeArrival BETWEEN '%s' and '%s';"""%(prev_time, current_time)

        err_msg = "unable fetching the most recent type command"

        return self.Execute_Select_Sql_Command(sql, err_msg)

    def Fetch_Topn_Unique_Commands(self, topn):
        sql = """SELECT cmdTxt as cmd, totalLearnability as score FROM unique_commands 
        ORDER BY score DESC LIMIT %d;"""%(topn)

        err_msg = "Failed to retrieve the topn unique commands..."
        return self.Execute_Select_Sql_Command(sql, err_msg)

    def Find_Most_Popular_Command(self):
        #find the most popular command where processed=0
        sql = """SELECT count(cmdLogID) as cmdCount, cmdTxt FROM command_log WHERE 
        processed =0 GROUP BY cmdTxt ORDER BY COUNT(cmdLogID) DESC LIMIT 1;"""

        err_msg = "Failed to fetch the most popular command..."
        result = self.Execute_SelectOne_Sql_Command(sql, err_msg)

        #change those commands as processed=1
        sql = """ UPDATE command_log SET processed=1 WHERE processed =0;"""
        self.Execute_Update_Sql_Command(sql)

        return result

    def Set_Current_Command(self, currentCommand):

        sql     = """SELECT * from unique_commands where active=1;"""
        err_msg = "Failed to fetch the previous command..."
        result = self.Execute_SelectOne_Sql_Command(sql, err_msg)

        prevCommand = ""
        if result!= None:
            prevCommand = result['cmdTxt']

        if prevCommand == currentCommand : return 

        sql= """ UPDATE unique_commands set active=1 WHERE cmdTxt='%s';"""%(currentCommand)
        err_msg = "Failed to set the current command..."
        self.Execute_Update_Sql_Command(sql, err_msg)

        sql= """UPDATE unique_commands set active=0 WHERE cmdTxt='%s';"""%(prevCommand)
        err_msg = "Failed to usnset the previous command..."
        self.Execute_Update_Sql_Command(sql, err_msg)

    def Get_Current_Command(self):

        sql= """SELECT * FROM unique_commands WHERE active=1;"""
        err_msg ="Failed to get the current command..."
        return self.Execute_SelectOne_Sql_Command(sql, err_msg)
