# Twitch Plays Robotics
The source code and data for Twitch Plays Robotics (TPR), a crowdsourcing project to teach robots natural language. This project is funded by the National Science Foundation and is run by a research team at the University of Vermont. 

## Pyrosim
We used a slightly modified version of Pyrosim, a Python wrapper above Open Dynamics Engine (ODE)
https://github.com/jbongard/pyrosim for our experiment.

## Core 

## Bots
##### chatBot.py
##### libraryBot.py
##### helpBot.py
##### database.py

## Twitch Chat Server
https://github.com/zmahoor/minimal-TPR

## Sensors
Each robot was displayed under a given command and a color on the broadcasting computer for 30 seconds. This 30 second period is called a robot evaluation. Sensor data for a robot evaluated at a specific time is stored in a file named,
    "robot_id_Year-month-day-hour-minute-second.dat". In the file name, id represents the robot's id, and "Year-month-day-hour-minute-second" shows the start time of the evaluation.

## Controllers

## Critic

## Database
###### Data stored in tables
We used MySQL to store and retrieve information of users, incoming messages, displaying robots in our experiments. The following sections explain the general schemas for the tables in our database.
### chats 
##### stores raw chat info

1. chatID:		The message number
2. timeArrival:		What time the message was stored
3. username:		Who typed it
4. txt:			What was in the message
5. processed:		Was it organized by library_bot? 0 for no
1 for yes

### command_log
##### stores commands typed in
1. cmdLogID:		The command order
2. userName:		Who typed the message
3. cmdTxt:		What the command is
4. timeArrival:		When it was stored
5. processed:		Flag **put something here**
6. animationFlag:	Flag **put something here**

### display
##### stores info about displayed robots
1. displayID:		Display order (unique number identifying each evaluation)
2. robotID:		What robot (robot table.1)
3. cmdTxt:		The command input
4. color:		What color the robot was displayed as
5. startTime:		When it started evaluation
6. numYes:		Number of positive reinforcements
7. numNo:		Number of negative reinforcements
8. numLike:		Number of likes
9. numDislike:		Number of dislikes

### helps
##### stores help messages
1. helpID:		Help message number (unique number)
2. txt:			What the message was
3. userName:		Who asked for help
4. timeArrival:		When the message was stored
5. processed:		Did help_bot respond? 0 for no
1 for yes

### reward_log
##### stores reward messages
1. rewardLogID:		Reward number (unique number)
2. userName:		Who typed the reward message
3. reward:			What it was (Y/N/L/D)
4. color:			What robot it was given to
5. timeArrival:		When it was received 
6. processed:		Flag **put something here**
7. displayID: the evaluation id that this reward was given for

### robots
##### stores robot info
1. robotID:			What number robot it is (unique number for each robot)
2. type:			The morphology
3. numEvals:		How many times it was evaluated
4. dead:			Is the robot dead (0 for no, 1 for yes)
5. totalFitness:	Robot's fitness
6. totalLikeability:Robot's likeability
7. birthDate:		When the robot was created
8. parentID:		Robot it was mutated from (0 for randomly generated)
9. deathDate:		When the robot died
10. sumYes: total yes's this robot has received
11. sumNo: total no's this robot has received
12. sumLike: total likes this robot has received
13. sumDislike: total dislikes this robot has received

### unique_commands
##### stores commands and their progress
1. cmdTxt:			What the command is
2. timeAdded:		When it was first typed
3. wordToVec:		[-1,1] using wordToVec algorithm
4. totalLearnability: How obedient the robots are to the command
5. active:			Are the robots currently acting on it (0 for no, 1 for yes)

### users
##### stores users and their scores
1. ID:				a unique number assigned to each user
2. userName:		The twitch username
3. timeAdded:		When they first typed a message
4. parentName: 		Who referred them
5. score:			The user's score (sum of all messages starting with a !)
6. ban:				Banned from the channel (0 for no, 1 for yes)


## More Information
https://tpr-uvm.github.io/

https://www.twitch.tv/twitchplaysrobotics
