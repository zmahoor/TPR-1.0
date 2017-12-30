(Work in progress) readme 

# Twitch Plays Robotics
The source code and data for Twitch Plays Robotics (TPR), a crowdsourcing project to teach robots natural language. This project is funded by the National Science Foundation and is run by a research team at the University of Vermont. 

## Pyrosim
We used a slightly modified version of Pyrosim, a Python wrapper above Open Dynamics Engine (ODE)
https://github.com/jbongard/pyrosim for our experiment.

To install Pyrosim, open a terminal window, and navigate into the pyrosim directory. For example:

```
$ cd ~/Desktop/TPR-1.0/pyrosim
```
Then run:
```
$ make
```
## Core 
##### steadyStateV4.py
1) This script dispays a window prompting users to type in reinforcement for a robot that is being displayed.
2) It also maintains the primary population of robots and evoloves the robots in the population 

##### fillDiversityPool.py
This script generates a secondary population of robots that feeds into the primary one.
To do so, it uses a hill climbing approach and novelty search to create diverse behaviours.

## Bots
##### chatBot.py
This script listens to a twitch channel and records any incoming message to the chat table.

##### libraryBot.py
This script reads all the unprocessed messages from the chat table and places them into their right tables.

##### helpBot.py
This script picks an unprocessed help message from the help table and sends a response to the user in the chat session.

##### scoreBot.py
This script wakes up every 10 seconds and updates score of all the users and commands.

##### commandWindow.py
This script displays a window prompting users to vote for the next command.

##### commandboard.py
This script displays a window of top 5 commands by score, or learnability.

##### leaderboard.py
This script displays a window of top 5 users by score.

##### database.py

## Twitch Chat Server
https://github.com/zmahoor/TPR-minimal helps you to start using twitch server for broadcasting and receiving/sending messages from/to a twitch channel.

## Sensors
Each robot was displayed under a given command and a color on the broadcasting computer for 30 seconds. This 30 second period is called a robot evaluation. Sensor data for a robot evaluated at a specific time is stored in a file named
"robot_id_Year-month-day-hour-minute-second.dat". In the file name, id represents the robot's id, and "Year-month-day-hour-minute-second" shows the start time of the evaluation.

Every sensor data file contains a pickled python dictionary of multiple elements (keys, values). Each element of this dictionary holds values of different sensors of a robot over its evaluation period. The key of the dictionary is a string which encodes a sensor type, and the value is a numpy array of length 1800 of the corresponding sensor values. The followings explain the keys to this dictionary.

A key starting with 'T' encodes a touch sensor,  a key starting with 'P' and ending with either 'X',  'Y', or 'Z' to a position sensor, a key starting with 'R' to a Ray (distance) sensor, and finally, a key starting with 'P' and ending with an integer to a proprioceptive (joint) sensor.

## Controllers
The controller of each robot displayed during the experiment is stored in this directory. This directory contains 10 subdirectories (one subdirectory per robot type). The name of a subdirectory maps to a robot type as follows: 1: twigbot, 2: stickbot, 3: branchbot, 4: treebot, shinbot: tablebot, starfishbot: starfishbot, crabbot: crabbot, quadruped: quadruped, snakebot: snakebot, spherebot: spherebot.

## Critic

## Database
We used MySQL to store and retrieve information of users, incoming messages, displaying robots in our experiments. The following sections explain the general schemas for the tables in our database.

###### Data stored in tables
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
https://arxiv.org/abs/1712.05881

https://tpr-uvm.github.io/

https://www.twitch.tv/twitchplaysrobotics
