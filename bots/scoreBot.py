from settings import *
import database
from time import sleep

mydatabase = database.DATABASE()


def main():
    while True:
        sleep(10.0)
        mydatabase.update_users_score()
        mydatabase.update_commands_score()

main()