from settings import *
import database;
from time import *
import re
from termcolor import colored

mydatabase = database.DATABASE();

def main():

    while True:

        users = mydatabase.Fetch_Top_Users(10)

        if users == None: continue

        print colored("Leaderboard----------------------", "green", attrs=['bold'])

        info = ("Rank" , "Useranme", "Score")
        txt = '{0:<10} {1:<15} {2:>5}'.format(*info)

        print colored(txt, "green", attrs=['bold'])
        print colored("---------------------------------", "green", attrs=['bold'])

        i = 1
        for user in users:
            user = (str(i), user['userName'], user['score'])
            txt = '{0:<10} {1:<15} {2:>06.2f}'.format(*user)
            print colored(txt, 'green')
            i += 1

        print

        for user in users:
            mydatabase.Update_Scores(user['userName'])
    
        sleep(30.0)

main()