import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()

sql = "select robotID, sum(numDislike) as numDislike, sum(numLike) as numLike from display group by robotID;"
records = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

count_disagreement = 0.0
count_total   = 0.0
count_dislike = 0.0
count_likes   = 0.0

for record in records:

	if record['numLike']>=1 and record['numDislike']>=1: count_disagreement += 1

	if record['numLike']>1 or record['numDislike']>1: count_total += 1

	if record['numLike']=0 and record['numDislike']>0: count_dislike += 1

	if record['numLike']>0 and record['numDislike']=0: count_like += 1


print count_disagreement, count_total, float(count_disagreement)/count_total

print ""




