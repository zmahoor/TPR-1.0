import sys
import matplotlib.pyplot as plt
sys.path.append('../bots')
from database import DATABASE

db = DATABASE()


data = {}
sql = """select numYes, numNo, robotID, displayID from TwitchPlays.display where (numYes+numNo)=1 and cmdTxt='stop';"""
records = db.execute_select_sql_command(sql, 'Failed fetch...')

for record in records:
    robotID = record['robotID']
    # print record

    if robotID in data:
        if record['numYes'] > 0: data[robotID] += 1
        if record['numNo'] > 0: data[robotID] -= 1
    else:
        if record['numYes'] > 0: data[robotID] = 1
        if record['numNo'] > 0: data[robotID] = -1

print len(records), len(data), data.values().count(0)

