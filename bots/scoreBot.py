from settings import *
import database;
from time import *
import re
from termcolor import colored

mydatabase = database.DATABASE();


def main():

    mydatabase.Update_Users_Score()

    mydatabase.Update_Commands_Score()

    # while True:

    #     topn = 10
    #     users = mydatabase.Fetch_Top_Users(topn)

    #     commands = mydatabase.Fetch_Top_Commands(topn)

    #     if users == None: continue

    #     print colored(" ----------Leaderboard-----------", "green", attrs=['bold'])

    #     info = ("Rank" , "Useranme", "Score")
    #     txt = '{0:<10} {1:<15} {2:>5}'.format(*info)

    #     print colored("|"+ txt + " |", "green", attrs=['bold'])
    #     print colored("|---------------------------------|", "green", attrs=['bold'])

    #     i = 1
    #     for user in users:
    #         user = (str(i), user['userName'], user['score'])
    #         txt = '{0:<10} {1:<15} {2:>06.2f}'.format(*user)
    #         print colored("|"+ txt + "|", 'green')
    #         i += 1
    #     print colored(" ---------------------------------", "green", attrs=['bold'])

    #     print


    #     print colored(" ----------Top Commands-----------", "blue", attrs=['bold'])

    #     info = ("Rank" , "Command", "Number")
    #     txt = '{0:<10} {1:<15} {2:>5}'.format(*info)

    #     print colored("|"+ txt + "|", "blue", attrs=['bold'])
    #     print colored("|---------------------------------|", "blue", attrs=['bold'])

    #     i = 1
    #     for cmd in commands:
    #         cmd = (str(i), cmd['cmdTxt'], cmd['totalLearnability'])
    #         txt = '{0:<10} {1:<15} {2:>6d}'.format(*cmd)
    #         print colored("|"+ txt + "|", 'blue')
    #         i += 1
    #     print colored(" ---------------------------------", "blue", attrs=['bold'])
    
    #     sleep(30.0)

main()