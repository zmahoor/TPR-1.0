import pymysql.cursors
import pymysql
from time import *
import datetime
from settings import *
import sys
import numpy as np
from collections import Counter


class DATABASE:

    def __init__(self):
        self.connect()

    def connect(self):
        """
        connect to the mysql db
        :return:
        """
        try:
            self.connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                                password=MYSQL_PASS, db=MYSQL_DB, connect_timeout=60)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("SELECT VERSION()")
            data = self.cursor.fetchone()
            print ("Database version : %s " %data)
        except Exception as e:
            print "Unable to connect to database...check your internet connection or the settings"
            print str(e)
            sys.exit()

    def close(self):
        """
        close the connection to mysql db
        :return:
        """
        try:
            self.connection.close()
            print 'closed the connection...'
        except:
            print 'Unable to close the connection...'

    def execute_update_sql_command(self, sql_command, err_msg=""):
        """
        execute an update sql command and display an error
        :param sql_command: string
        :param err_msg: string
        :return: results
        """
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()

        except KeyboardInterrupt:
            self.connection.rollback()
            sys.exit()

        except (pymysql.OperationalError, pymysql.InternalError), e:
            self.connect()
            print str(e)

        except pymysql.ProgrammingError, e:
            print str(e)
            print (err_msg)

    def execute_select_sql_command(self, sql_command, err_msg=""):
        """
        execute a select sql command
        :param sql_command: string
        :param err_msg: string
        :return: list of dictionaries
        """
        results = None
        try:
            self.cursor.execute(sql_command)
            results = self.cursor.fetchall()
            self.connection.commit()
        except KeyboardInterrupt:
            self.close()
            sys.exit()
        except (pymysql.OperationalError, pymysql.InternalError), e:
            self.connect()
            print str(e)
        except pymysql.ProgrammingError, e:
            print str(e)
            print (err_msg)
        return results

    def execute_select_one_sql_command(self, sql_command, err_msg=""):
        """
           execute a select sql command
           :param sql_command: string
           :param err_msg: string
           :return: dictionary
        """
        results = None
        try:
            self.cursor.execute(sql_command)
            results = self.cursor.fetchone()
            self.connection.commit()
        except KeyboardInterrupt:
            self.close()
            sys.exit()
        except (pymysql.OperationalError, pymysql.InternalError), e:
            print(err_msg)
            print str(e)
            self.connect()
        except pymysql.ProgrammingError, e:
            print(err_msg)
            print str(e)

        return results

    def add_to_chat_table(self, username, current_time, msg):
        """
        Insert username, message and current time to the chat table.
        :param username: string
        :param current_time: datetime
        :param msg: string
        :return: none
        """
        sql = """INSERT INTO chats(timeArrival, username, txt) VALUES ('%s', '%s', '%s');"""%(current_time, username, msg)
        self.execute_update_sql_command(sql, "Failed to insert the chat message...")
    
    def add_to_help_table(self, user, txt, time):
        """
        insert user, txt and time to the help table.
        :param user: string
        :param txt: string
        :param time: datetime
        :return: none
        """
        sql = """INSERT INTO helps(txt, userName, timeArrival) VALUES('%s','%s','%s');"""%(txt, user, time)
        self.execute_update_sql_command(sql, "Failed to insert help request..")

    def add_to_user_table(self, username, time):
        """
        insert user, and time to the user table.
        :param username: string
        :param time: string
        :return: none
        """
        sql = """INSERT IGNORE INTO users(userName, timeAdded) VALUES('%s', '%s');""" %(username, time)
        self.execute_update_sql_command(sql, "Failed to insert a new user...")
        
    def add_reward_to_display_table(self, color, reward, arrivalTime):
        """
        insert reward, color and time to the display table
        :param color: string
        :param reward: string
        :param arrivalTime: datetime
        :return: none
        """
        # if the startTime is beyond 2 minutes, discard this reward
        if reward == 'y':
            sql = """ UPDATE display set numYes=numYes+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;""" %(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE display set numNo=numNo+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;""" %(color, arrivalTime)

        elif reward == 'l':
            sql = """ UPDATE display set numLike=numLike+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;""" %(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE display set numDislike=numDislike+1 WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)

        else: return
        self.execute_update_sql_command(sql,
                                        "Failed to insert the reward into the display table...")

    def add_to_Reward_log_table(self, username, color, reward, arrivalTime):
        """
        insert username, color, reward and time to the reward_log table.
        :param username: string
        :param color: string
        :param reward: string
        :param arrivalTime: datetime
        :return:
        """
        sql = """SELECT displayID from display WHERE color='%s' and '%s' BETWEEN startTime
             and startTime+INTERVAL 2 MINUTE ORDER BY startTime DESC LIMIT 1;"""%(color, arrivalTime)
        result = self.execute_select_one_sql_command(sql, "Failed adding reward to log table.")

        if result is None or result['displayID'] is None:
            displayID = -1
        else:
            displayID = result['displayID']

        sql = """INSERT INTO reward_log(userName, reward, color, timeArrival, displayID) VALUES
        ('%s', '%s', '%s', '%s', '%d');"""%(username, reward, color, arrivalTime, displayID)
        self.execute_update_sql_command(sql, "Failed to log this reward...")

    def add_to_command_log_table(self, username, command, time):
        """
        insert username, command, and time to the command_log table
        :param username: string
        :param command: string
        :param time: datetime
        :return: none
        """

        sql = """INSERT INTO command_log(userName, cmdTxt, timeArrival) VALUES
        ('%s', '%s', '%s');"""%(username, command, time)
        self.execute_update_sql_command(sql, "Failed to log this command...")

    def add_to_unique_commands_table(self, command, time, wordToVec, active=0):
        """
        insert command, time, vector, active flag(0 or 1) to the unique command table.
        :param command: string
        :param time: datetime
        :param wordToVec: float
        :param active: int
        :return: none
        """
        sql = """INSERT IGNORE INTO unique_commands(cmdTxt, timeAdded, 
            wordToVec, totalLearnability, active) VALUES
            ('%s', '%s', '%f', 0, '%d');"""%(command, time, wordToVec, active)
        self.execute_update_sql_command(sql, "Failed to add this new command...")

    def add_to_robot_table(self, robotType, parentID=0):
        """
        insert the robot type with parent id into th robot table.
        :param robotType: string
        :param parentID: int
        :return: none
        """
        robotID = 0
        birthDate = datetime.datetime.now()
        birthDate = birthDate.strftime("%Y-%m-%d %H:%M:%S")

        sql = """INSERT INTO robots(type, birthDate, parentID) VALUES('%s', '%s', '%d');"""%(robotType, birthDate, parentID)

        try:
            self.cursor.execute(sql)
            robotID = self.connection.insert_id()
            self.connection.commit()
        except:
            self.connection.rollback()
            print("Failed to insert the robot into the robots table...")

        return robotID

    def add_command_to_display_table(self, robotID, cmdTxt, color, startTime):
        """
        insert robotID, command, color and time into the display table.
        :param robotID: int
        :param cmdTxt: string
        :param color: string
        :param startTime: date
        :return: none
        """
        startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")

        sql = """INSERT INTO display(robotID, cmdTxt, color, startTime) VALUES
        ('%d','%s','%s', '%s');"""%(robotID, cmdTxt, color, startTime)

        err_msg = "Failed to insert a robot into the display table..."
        self.execute_update_sql_command(sql, err_msg)

        sql = "UPDATE robots SET numEvals=numEvals+1 WHERE robotID='%d';"%(robotID)
        self.execute_update_sql_command(sql, "Failed to update number of "
                                             "evaluations for a robot...")

    def flush_old_unprocessed_helps(self):
        """
        update all the rows of the help table with processed=1
        :return: none
        """
        sql = "UPDATE helps SET processed=1 WHERE processed=0;"
        self.execute_update_sql_command(sql)

    def flush_old_unprocessed_chats(self):
        """
        update all the rows of the chats table with processed=1
        :return: none
        """
        sql = "UPDATE chats SET processed=1 WHERE processed=0;"
        self.execute_update_sql_command(sql)

    def update_user_parent(self, user, parent):
        """
        update the parent of user
        :param user: string
        :param parent: string
        :return: none
        """
        sql = """UPDATE users set parentName='%s' WHERE userName='%s' 
        and parentName is NULL;"""%(parent, user)
        self.execute_update_sql_command(sql, "Failed to update the user's parent...")

    def update_robot_feedback(self, color, reward, arrivalTime):
        """
        update
        :param color: string
        :param reward: string
        :param arrivalTime: datetime
        :return: none
        """
        if reward == 'y':
            sql = """ UPDATE robots set sumYes=sumYes+1 WHERE 
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'n':
            sql = """ UPDATE robots set sumNo=sumNo+1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)
        
        elif reward == 'l':
            sql = """ UPDATE robots set sumLike=sumLike+1 WHERE 
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        elif reward == 'd':
            sql = """ UPDATE robots set sumDislike=sumDislike+1 WHERE
            robotID = (SELECT robotID FROM display WHERE color='%s'
            and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
             ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)

        else: return
        self.execute_update_sql_command(sql, "Failed to update the robot's fitness...")

    # def Update_Total_Fitness(self, color, reward, arrivalTime):
    #     if reward == 'y':
    #         sql = """ UPDATE robots set totalFitness=totalFitness+1 WHERE
    #         robotID = (SELECT robotID FROM display WHERE color='%s'
    #         and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
    #          ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)
    #
    #     elif reward == 'n':
    #         sql = """ UPDATE robots set totalFitness=totalFitness-1 WHERE
    #         robotID = (SELECT robotID FROM display WHERE color='%s'
    #         and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
    #          ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)
    #
    #     else: return
    #
    #     err_msg = "Failed to update the robot's fittness..."
    #     self.Execute_Update_Sql_Command(sql, err_msg)
    #
    # def Update_Total_Likeability(self, color, reward, arrivalTime):
    #     if reward == 'l':
    #         sql = """ UPDATE robots set totalLikeability=totalLikeability+1 WHERE
    #         robotID = (SELECT robotID FROM display WHERE color='%s'
    #         and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
    #          ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)
    #
    #     elif reward == 'd':
    #         sql = """ UPDATE robots set totalLikeability=totalLikeability-1 WHERE
    #         robotID = (SELECT robotID FROM display WHERE color='%s'
    #         and '%s' BETWEEN startTime and startTime + INTERVAL 2 MINUTE
    #          ORDER BY startTime DESC LIMIT 1);"""%(color, arrivalTime)
    #
    #     else: return
    #
    #     err_msg = "Failed to update the robot's fittness..."
    #     self.Execute_Update_Sql_Command(sql, err_msg)

    def update_users_score(self):
        """
        update all the users' scores
        :return: none
        """

        sql = """SELECT * from users;"""
        err_msg = "Failed to fetch all usernames..."
        records = self.execute_select_sql_command(sql, err_msg)

        if records is None:
            return

        for row in records:
            user = row['userName']
            # print user
            sql = """UPDATE users SET score=(SELECT count(*) FROM reward_log WHERE
             userName = '%s') + (SELECT count(*) FROM command_log WHERE
             userName = '%s') WHERE userName = '%s' ;""" %(user, user, user)
            
            err_msg = "Failed to update user's score..."
            self.execute_update_sql_command(sql, err_msg)

    def update_commands_score(self):
        """
        update all the commands' scores according to (Y_2 - N_2) - (Y_1 - N_1)
        :return: none
        """
        sql = """ SELECT cmdTxt, min(startTime) as firstTime, max(startTime) as lastTime
            from display group by cmdTxt;"""
        err_msg = "Faild to fetch command names..."
        records = self.execute_select_sql_command(sql, err_msg)

        if records is None:
            return

        for row in records:
            # print row
            command = row['cmdTxt']
            start_time, last_time = row['firstTime'], row['lastTime']
            first_sum, second_sum = 0, 0
            mid_time = start_time + (last_time-start_time)/2
            # print mid_time

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as firstSum FROM 
                    display WHERE startTime <= '%s' and cmdTxt='%s';"""%(mid_time, command)
            err_msg = "Failed to fetch command names"
            result = self.execute_select_one_sql_command(sql, err_msg)

            if result['cmdTxt'] is not None:
                first_sum = result['firstSum']

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as secondSum FROM
             display WHERE startTime > '%s' and cmdTxt='%s';"""%(mid_time, command)
            result = self.execute_select_one_sql_command(sql)

            if result['cmdTxt'] is not None:
                second_sum = result['secondSum']

            sql = """UPDATE unique_commands SET totalLearnability ='%f' WHERE 
                cmdTxt ='%s';"""%(second_sum - first_sum, command)
            err_msg = "Failed to update command's learnability"
            self.execute_update_sql_command(sql, err_msg)

    def kill_robot(self, robotID):
        """
        change the given robot's dead flag to 1 (kill it)
        :param robotID: int
        :return: none
        """
        deathDate = datetime.datetime.now()
        deathDate = deathDate.strftime("%Y-%m-%d %H:%M:%S")

        sql = """UPDATE robots set dead=1, deathDate='%s' WHERE 
        robotID=%d;"""%(deathDate, robotID)
        err_msg = "Failed to kill the robot..."
        self.execute_update_sql_command(sql, err_msg)

    def get_new_word_vector(self):
        """
        find a unique number for a new command within the range (-1, +1)
        :return: int
        """
        sql="""SELECT wordToVec FROM unique_commands;"""
        err_msg = "unable to fetch user names"
        results = self.execute_select_sql_command(sql, err_msg)

        newIndex = 0
        if results is not None:
            newIndex = 2*np.random.random()-1

            while newIndex in results:
                newIndex = 2*np.random.rand()-1
        else:
            newIndex = 2*np.random.random()-1
        return newIndex

    def count_evaluations_for_command(self, currentCommand):
        """
        find the number of evaluations for all alive robots under currentCommand
        :param currentCommand: string
        :return: counter
        """
        sql = """select d.robotID from TPR_Sept.display as d
         join TPR_Sept.robots as r on d.robotID=r.robotID where cmdTxt='%s' and 
         dead=0;""" %(currentCommand)
        # print sql
        result = self.execute_select_sql_command(sql, "Not able to fetch.")
        # print result
        if result is () or result is None:
            return None
        return Counter([r['robotID'] for r in result])

    def fetch_user_feedback(self, username):
        """
        find the number of rewards entered by username grouped by type
        :param username: string
        :return: List[Dict]
        """
        sql = """select count(*) as num, reward as feedback_type from reward_log
         where userName='%s' group by reward;"""%(username)
        return self.execute_select_sql_command(sql,
                                               'Failed fetching feedback info for a user.')

    def fetch_robot_information(self):
        """
        find the information to display for the most recent evaluation
        :return: Dict
        """
        sql = """SELECT d.robotID, d.cmdTxt, d.color, r.type, r.birthDate, r.parentID from display as d
         join robots as r ON d.robotID=r.robotID order by d.startTime desc limit 1;"""
        result = self.execute_select_one_sql_command(sql, 'Failed fetching info for a robot')

        if result is None:
            return None

        robotID, cmdTxt, robotType = result['robotID'], result['cmdTxt'], result['type']

        # find num of yes's and num of no's from the display table for a given robotID and command
        sql = """SELECT sum(numYes) as numYes, sum(numNo) as numNo from display where
         robotID='%d' and cmdTxt ='%s';""" %(robotID, cmdTxt)
        result1 = self.execute_select_one_sql_command(sql, 'Failed fetching info for a robot')

        if result1 is not None:
            result.update(result1)

        # find the number of alive robots of given type from the robot table
        sql = """SELECT count(*) as numOfKind, type as robotType from robots where
         type='%s' and dead=0;""" %(robotType)
        result2 = self.execute_select_one_sql_command(sql, 'Failed fetching info for a robot')

        if result2 is not None:
            result.update(result2)

        # find the first time and the last time from the display table given robotID
        sql = """SELECT min(startTime) as firstDisplay, max(startTime) as lastDisplay
         from display where robotID='%d' """ %(robotID)
        result3 = self.execute_select_one_sql_command(sql, 'Failed fetching info for a robot')

        if result3 is not None:
            result.update(result3)

        # find num of like's and num of dislike's from the display table for a given robotID
        sql = """SELECT sum(numDislike) as numDislike, sum(numLike) as numLike from 
        display where robotID='%d';""" %(robotID)
        result4 = self.execute_select_one_sql_command(sql, 'Failed fetching info for a robot')

        if result4 is not None:
            result.update(result4)

        return result

    def fetch_for_abuse_bot(self):
        """
        find all usernames and typed commands from the command_log table within the 24 hours
        :return: list[dict]
        """
        sql = """select userName, cmdTxt from command_log where 
        timeArrival>=NOW() - interval 24 hour;"""
        return self.execute_select_sql_command(sql, 'Unable fetching from the command log.')

    def fetch_from_display_table(self, condition='all'):
        """
        find robotID, robot type, command, command vector, num yes's, num no's, num of likes, num of dislikes, num of likes
        :param condition: string
        :return: list[dict]
        """
        if condition == 'all':
            sql = """SELECT d.robotID, r.type, d.cmdTxt, u.wordToVec, 
            d.numYes, d.numNo, d.numLike, d.numDislike, d.startTime
            from display as d JOIN robots as r ON d.robotID=r.robotID 
            JOIN unique_commands as u on d.cmdTxt=u.cmdTxt;"""

        # all the rows of the display table with yes's>0 and no's>0
        elif condition == 'all_yes_or_no':
            sql = """SELECT d.robotID, r.type, d.cmdTxt, u.wordToVec, 
            d.numYes, d.numNo, d.numLike, d.numDislike, startTime
            from display as d JOIN robots as r ON d.robotID=r.robotID 
            JOIN unique_commands as u on d.cmdTxt=u.cmdTxt
            WHERE d.numNo <> 0 or d.numYes <> 0;"""

        err_msg = "Failed to retrieve record of a dispaly..."
        return self.execute_select_sql_command(sql, err_msg)

    def fetch_user_score(self, user):
        """
        find a user's score
        :param user: string
        :return: dict
        """
        sql = "SELECT * FROM users WHERE userName='%s';"%user
        err_msg = "Failed to retrieve a user's score"
        return self.execute_select_one_sql_command(sql, err_msg)

    def fetch_top_users(self, topn):
        """
        find the top n users from the users table
        :param topn: int
        :return: list[dict]
        """
        if topn == 'all':
            sql = """SELECT userName, score FROM users ORDER BY score DESC;"""
        else:
            sql = """SELECT userName, score FROM users ORDER BY score DESC LIMIT %d;""" %(topn)

        err_msg = "Failed to retrieve scores of top users..."
        return self.execute_select_sql_command(sql, err_msg)

    def fetch_top_daily_users(self, topn):
        """
            find the top n users from the users table (highest scores during the last day)
            :param topn: int
            :return: list[dict]
        """
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%Y-%m-%d 00:00:00")

        sql = """SELECT userName, score FROM users where userName in 
        (SELECT distinct username FROM chats WHERE timeArrival BETWEEN '%s' and '%s'+interval 1 day)
        ORDER BY score DESC LIMIT %d;"""%(current_time, current_time, topn)

        err_msg = "Failed to retrieve scores of top users..."
        return self.execute_select_sql_command(sql, err_msg)

    def fetch_recent_typed_command(self, interval=10):
        """
        return a list of all commands along with their scores and ranks
        that were typed (interval) seconds before the current time
        :param interval: int
        :return: list[dict]
        """
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
        return self.execute_select_sql_command(sql, err_msg)

    def fetch_recent_active_users(self, interval=10):
        """
        return a list of all active users with the past n seconds along with their scores and ranks
        :param interval: int
        :return: list[dict]
        """
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
        return self.execute_select_sql_command(sql, err_msg)


    def fetch_alive_robots(self, robotType="all"):
        """
        find all the robots with the dead flag as zero (zero: alive, one:dead)
        :param robotType:
        :return:
        """
        if robotType == "all":
            sql = "SELECT * FROM robots WHERE dead=0;"
        else:
            sql = "SELECT * FROM robots WHERE dead=0 and type='%s';" %(robotType)

        err_msg = "Failed to retrieve alive robots..."
        return self.execute_select_sql_command(sql, err_msg)

    def fetch_unprocessed_chat(self):
        """
        find the oldest piece of unprocessed chat
        update the processed flag as 1 for that piece of chat
        :return: dict
        """
        sql = "SELECT * FROM chats WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
        result = self.execute_select_one_sql_command(sql)

        if result is not None:
            chatID = result['chatID']
            sql = "UPDATE chats SET processed=1 WHERE chatID='%d';" %(chatID)
            self.execute_update_sql_command(sql)

        return result

    def fetch_oldest_help(self):
        """
        find the last unprocessed help form the help table
        :return: dict
        """
        sql = "SELECT * FROM helps WHERE processed=0 ORDER BY timeArrival ASC LIMIT 1;"
        err_msg = "Failed to fetch the oldest unprocessed help request..."
        result = self.execute_select_one_sql_command(sql, err_msg)

        if result is not None:
            helpID = result['helpID']
            sql = "UPDATE helps SET processed=1 WHERE helpID='%d';" %(helpID)
            self.execute_update_sql_command(sql, err_msg)

        return result
        
    def first_time_contributer(self, username):
        """
        return true if this user has ever typed a reward or command;
        otherwise false
        :param username: string
        :return: Bool
        """
        sql = """SELECT userName FROM reward_log where userName='%s' union 
        SELECT userName FROM command_log where userName='%s';""" %(username, username)
        err_msg = "Failed to fetch information about this user..."
        result = self.execute_select_sql_command(sql, err_msg)

        if result == (): 
            return True
        
        return False

    def tobe_animated_in_command_window(self):
        """
        return username, command, time from the command_log table where animation flag is zero
        :return: list[dict]
        """
        sql = """SELECT userName, cmdTxt, timeArrival FROM command_log WHERE animationFlag=0;"""
        err_msg = "unable fetching the most recent type command"
        result = self.execute_select_sql_command(sql, err_msg)

        sql = """ UPDATE command_log SET animationFlag=1 WHERE animationFlag=0;"""
        self.execute_update_sql_command(sql)

        return result

    def fetch_for_command_window(self, interval=10):
        """
        find username, command, time from the command_log table within the past "interval" seconds.
        :param interval: int
        :return: list[dict]
        """
        current_time = datetime.datetime.now()
        prev_time = current_time - datetime.timedelta(seconds=interval)

        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")

        sql = """SELECT userName, cmdTxt, timeArrival FROM command_log
        WHERE timeArrival BETWEEN '%s' and '%s';""" %(prev_time, current_time)
        err_msg = "unable fetching the most recent type command"

        return self.execute_select_sql_command(sql, err_msg)

    def fetch_topn_unique_commands(self, topn):
        """
        find the top n commands and their learnability score from the unique_command table
        :param topn: int
        :return: list[dict]
        """
        if topn == 'all':
            sql = """SELECT cmdTxt as cmd, totalLearnability as score FROM unique_commands 
            ORDER BY score;"""
        else:
            sql = """SELECT cmdTxt as cmd, totalLearnability as score FROM unique_commands 
            ORDER BY score DESC LIMIT %d;""" %topn

        err_msg = "Failed to retrieve the top n unique commands..."
        return self.execute_select_sql_command(sql, err_msg)

    def find_most_voted_command(self):
        """
        find the most popular command with processed=0 and change those commands to processed=1
        :return: none
        """
        sql = """SELECT count(cmdLogID) as cmdCount, cmdTxt FROM command_log WHERE 
        processed =0 GROUP BY cmdTxt ORDER BY COUNT(cmdLogID) DESC LIMIT 1;"""
        err_msg = "Failed to fetch the most popular command..."
        result = self.execute_select_one_sql_command(sql, err_msg)

        sql = """ UPDATE command_log SET processed=1 WHERE processed=0;"""
        self.execute_update_sql_command(sql)

        return result

    def set_current_command(self, currentCommand):
        """
        find the current active command and deactivate it
        then set currentCommand as the active command
        :param currentCommand: string
        :return: none
        """
        # find the current active command
        sql = """SELECT * from unique_commands where active=1;"""
        err_msg = "Failed to fetch the previous command..."
        result = self.execute_select_one_sql_command(sql, err_msg)

        prevCommand = ""
        if result is not None:
            prevCommand = result['cmdTxt']

        if prevCommand == currentCommand:
            return

        # set the current command as active
        sql = """ UPDATE unique_commands set active=1 WHERE cmdTxt='%s';""" %currentCommand
        err_msg = "Failed to set the current command..."
        self.execute_update_sql_command(sql, err_msg)

        # deactivate the previous active command
        sql= """UPDATE unique_commands set active=0 WHERE cmdTxt='%s';""" %prevCommand
        err_msg = "Failed to usnset the previous command..."
        self.execute_update_sql_command(sql, err_msg)

    def get_current_command(self):
        """
        find the command with active=1
        :return: dict
        """
        sql = """SELECT * FROM unique_commands WHERE active=1;"""
        err_msg = "Failed to get the current command..."
        return self.execute_select_one_sql_command(sql, err_msg)
