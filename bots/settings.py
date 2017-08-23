#twitch info
HOST    = "irc.twitch.tv"
PORT    = 6667
PASS    = "oauth:en2uoj77da5z68rnufdhpculxd1qbo"
IDENT   = "tpr_bot2"
CHANNEL = "twitchplaysrobotics"

#mysql info
MYSQL_HOST = '132.198.138.119'
MYSQL_DB   = 'TwitchPlays'
MYSQL_USER = 'root'
MYSQL_PASS = 'twitchplaysrobotics2138'

#simulator info
validColors   = ['red', 'green', 'blue', 'orange', 'cyan', 'purple']
specialColor  = 'silver'
filteredUsers = ["tpr_bot2", "tpr_bot1", "tpr_bot3", "tpr_bot"]
# validRobots   = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',\
#  'spherebot', 'snakebot', 'crabbot', 'humanoid', 'snakeplusbot', 'quadrupedplus',\
#  'crabplusbot']

validRobots   = ['3', '4']

maxCommandLength = 100
minCommandLength = 3
DEFAULT_COMMAND  = "move"
