#!/bin/bash
RSYNC=/usr/bin/rsync
SSH=/usr/bin/ssh
CD=/usr/bin/cd

#-------------------------To be set by user-------------------------------------
LOCAL_DIR="/Users/twitchplaysrobotics/TPR-1.0"
REMOTE_DIR="/Users/twitchplaysrobotics/TPR-1.0"

VADER1="132.198.138.119"
USERNAME="twitchplaysrobotics"

robot=$1
$CD ~/TPR-1.0/pyrosim; python -u fillDiversityPool.py -r $robot -p 20 -t 55 -b 5 &> tmp/diversity_$robot.log && 
$RSYNC --remove-source-files -avzh ~/TPR-1.0/diversity_pool/$robot/ $USERNAME@$VADER1$:~/TPR-1.0/diversity_pool/$robot