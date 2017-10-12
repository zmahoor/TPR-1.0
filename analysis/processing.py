import sys 

sys.path.append('../bots')

from database import DATABASE

path_to_log    = "/Users/twitchplaysrobotics/TPR-1.0/pyrosim/tmp/steadystate_14.log"

db = DATABASE()

with open(path_to_log, 'r') as input_file:

    for line in input_file:

        if line.startswith('Current time: '):
            death_time = line[line.index(':')+3:line.index('.')]

        if line.startswith('Loser is: '):
            loser_id = int(line[line.index(':')+3:len(line)-1])

            print loser_id, death_time

            sql = """UPDATE robots set deathDate='%s' where robotID='%d';"""%(death_time, loser_id)

            db.execute_update_sql_command(sql, err_msg="Falid to update: %d" % (loser_id))

injectd  = False

with open(path_to_log, 'r') as input_file:

    for line in input_file:

        if line.startswith('To be killed'):
            loser_id = line[line.find("ID':")+5:line.find(", u'birthDate'")]
            loser_id = int(loser_id)
            injectd  = True

        if injectd and line.startswith('Current time: '):
            death_time = line[line.index(':')+3:line.index('.')]
            new_line = str(loser_id) + ' ' + death_time + '\n'
            injectd  = False

            print loser_id, death_time

            sql = """UPDATE robots set deathDate='%s' where robotID='%d';"""%(death_time, loser_id)

            db.execute_update_sql_command(sql, err_msg="Falid to update: %d" % (loser_id))
