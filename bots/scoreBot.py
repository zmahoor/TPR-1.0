from settings import *
import database
from time import sleep

mydatabase = database.DATABASE();


def main():

    while True:

        sleep(10.0)

        mydatabase.Update_Users_Score()

        mydatabase.Update_Commands_Score()

main()