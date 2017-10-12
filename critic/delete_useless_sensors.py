import sys 
import os

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()

def Delete_Sensor_File(record):

    robotID   = record['robotID']
    startTime = record['startTime']
    
    path = main_path + "/sensors/" + str(startTime.year) + "/" + str(startTime.month) +\
        "/" + str(startTime.day) + "/robot_" + str(robotID) + '_' +\
         startTime.strftime("%Y-%m-%d-%H-%M-%S") + ".dat"

    # print path

    if not os.path.isfile(path): 
        print "not found: ", path
        return

    try:
        print "fileToBeRemoved: ", path
        os.remove(path)

    except Exception as e:
        print str(e), path

def Delete_Useless_Sensor_Files():

    records = mydatabase.fetch_from_display_table('all')

    delete_count = 0

    for record in records:

        if record['numYes'] == 0 and record['numNo'] == 0 and \
            record['numLike'] ==0 and record['numDislike'] == 0:

            # print 'zero feedback...removing it.'

            Delete_Sensor_File(record)

            delete_count += 1

    print "to be deleted: ", delete_count

main_path = "/Users/twitchplaysrobotics/TPR-backup"

Delete_Useless_Sensor_Files()