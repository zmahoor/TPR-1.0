import sys
sys.path.append('../bots')

from database import DATABASE

db = DATABASE()

# sql="""SELECT sum(numYes) as sumYes, sum(numNo) as sumNo, sum(numLike) as 
# sumLike, sum(numDislike) as sumDislike, robotID
#  FROM TwitchPlays.display  group by robotID;"""

# robots = db.Execute_Select_Sql_Command(sql , "failed all the information.")

# for robot in robots:

#     sumYes     = robot['sumYes']
#     sumNo      = robot['sumNo']
#     sumLike    = robot['sumLike']
#     sumDislike = robot['sumDislike']
#     robotID    = robot['robotID']

#     sql = """UPDATE robots set sumYes=%d, sumNo=%d, sumLike=%d, sumDislike=%d
#     where robotID=%d ;"""%(sumYes, sumNo, sumLike, sumDislike, robotID)

#     db.Execute_Update_Sql_Command(sql, err_msg="Falid to update: %d"%(robotID) )

sql=""" SELECT displayID, robotID, color, startTime FROM TwitchPlays.display;"""
evaluations = db.Execute_Select_Sql_Command(sql , "failed all the information.")

for evaluation in evaluations:

    displayID = evaluation['displayID']
    startTime = evaluation['startTime']
    color     = evaluation['color']

    # print startTime, color,

    # sql="""SELECT rewardLogID, timeArrival, color from TwitchPlays.reward_log where timeArrival between
    # '%s' and '%s'+interval 1 minute and color='%s';"""%(startTime, startTime, color)
    # records = db.Execute_Select_Sql_Command(sql , "failed all the information.")

    sql="""UPDATE TwitchPlays.reward_log set displayID=%d where timeArrival between
    '%s' and '%s'+interval 2 minute and color='%s';"""%(displayID, startTime, startTime, color)
    db.Execute_Update_Sql_Command(sql, err_msg="Falid to update: %d"%(displayID) )

    # print records


