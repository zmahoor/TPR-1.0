#twitch info
HOST    = "irc.twitch.tv"
PORT    = 6667
PASS    = "oauth:en2uoj77da5z68rnufdhpculxd1qbo"
IDENT   = "tpr_bot2"
CHANNEL = "mungozero"

#mysql info
# MYSQL_HOST = '45.79.171.136'
MYSQL_HOST = '132.198.138.134'
MYSQL_DB   = 'TwitchPlays'
MYSQL_USER = 'root'
MYSQL_PASS = 'twitchplaysrobotics2138'

#simulator info
validColors   = ['red', 'green', 'blue', 'orange', 'cyan', 'purple']
filteredUsers = ["tpr_bot2", "tpr_bot1", "tpr_bot3", "tpr_bot"]
validRobots   = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',\
 'spherebot', 'snakebot', 'crabbot']

maxCommandLength = 50
minCommandLength = 2
DEFAULT_COMMAND  = "move"
