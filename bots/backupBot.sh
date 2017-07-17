#!/bin/bash
RSYNC=/usr/bin/rsync
SSH=/usr/bin/ssh
MYSQLDUMP=/usr/local/bin/mysqldump
#-------------------------To be set by user-------------------------------------
MAIN_DIR="/Users/twitchplaysrobotics/TPR-1.0"
BACKUP_DIR="/Users/twitchplaysrobotics/TPR-backup"
MAINDIR="/backup_tpr"

USERNAME="root"
DBNAME="TwitchPlays"
PASS="twitchplaysrobotics2138"

EXT=".sql.gz"
THRESHOLD=24
#-------------------------------------------------------------------------------

MAIN_SENSORS_DIR="$MAIN_DIR/sensors/"
MAIN_CONTROLLERS_DIR="$MAIN_DIR/controllers/"
MAIN_DB_DIR="$MAIN_DIR/db/"

BACKUP_SENSORS_DIR="$BACKUP_DIR/sensors"
BACKUP_CONTROLLERS_DIR="$BACKUP_DIR/controllers"
BACKUP_DB_DIR="$BACKUP_DIR/db"

mkdir -p $BACKUP_DIR

echo $MAIN_SENSORS_DIR
echo $BACKUP_SENSORS_DIR

DBFILE=${MAIN_DB_DIR}db_$(date +'%Y-%m-%d-%H')$EXT
$MYSQLDUMP --opt --user=${USERNAME} --password=${PASS} ${DBNAME} | gzip > ${DBFILE}  

cd $MAIN_DB_DIR; ls -tp *$EXT| grep -v '/$' | tail -n +$(($THRESHOLD+1)) | tr '\n' '\0' | xargs -0 rm --; cd -

#send the sensors produced in the previous hour to the cloud
$RSYNC -avzh ${MAIN_SENSORS_DIR} ${BACKUP_SENSORS_DIR}

#send the controllers produced in the previous hour to the cloud
$RSYNC -avzh ${MAIN_CONTROLLERS_DIR} ${BACKUP_CONTROLLERS_DIR}

#store the most recent backup of the database from the cloud
$RSYNC -avzh ${MAIN_DB_DIR} ${BACKUP_DB_DIR} 

cd $BACKUP_DB_DIR; ls -tp *$EXT| grep -v '/$' | tail -n +$(($THRESHOLD+1)) | tr '\n' '\0' | xargs -0 rm --; cd -
