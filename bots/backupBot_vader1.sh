#!/bin/bash
RSYNC=/usr/bin/rsync
SSH=/usr/bin/ssh
#-------------------------To be set by user-------------------------------------
REMOTE_HOST="45.79.171.136"
REMOTE_USERNAME="root"

LOCAL_MAIN_DIR="/Users/zahra/TPR"
REMOTE_MAIN_DIR="/backup_tpr"
#-------------------------------------------------------------------------------
PREV_YEAR="$(date -v -1H '+%Y')"
PREV_MONTH="$(date -v -1H '+%m')"
PREV_DAY="$(date -v -1H '+%d')"
PREV_HOUR="$(date -v -1H '+%H')"

LOCAL_SENSORS_DIR="$LOCAL_MAIN_DIR/sensors/$PREV_YEAR/$PREV_MONTH/$PREV_DAY/$PREV_HOUR/"
LOCAL_CONTROLLERS_DIR="$LOCAL_MAIN_DIR/controllers/$PREV_YEAR/$PREV_MONTH/$PREV_DAY/$PREV_HOUR/"
LOCAL_DB_DIR="$LOCAL_MAIN_DIR/db"

REMOTE_SENSORS_DIR="$REMOTE_MAIN_DIR/sensors/$PREV_YEAR/$PREV_MONTH/$PREV_DAY/$PREV_HOUR"
REMOTE_CONTROLLERS_DIR="$REMOTE_MAIN_DIR/controllers/$PREV_YEAR/$PREV_MONTH/$PREV_DAY/$PREV_HOUR/"
REMOTE_DB_DIR="$REMOTE_MAIN_DIR/db"

echo $REMOTE_SENSORS_DIR
echo $LOCAL_SENSORS_DIR

# SENSOR_FILE="s$(date -v -1H '+%Y%m%d%H').tar.gz"

# tar -czvf ${COMPRESSED_FILE} -C $LOCAL_SENSORS_DIR .
# ssh ${REMOTE_USERNAME}@${REMOTE_HOST} "mkdir -p $REMOTE_SENSORS_DIR" && scp ${SENSOR_FILE} ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_SENSORS_DIR}
# rm  ${SENSOR_FILE}

# ssh ${REMOTE_USERNAME}@${REMOTE_HOST} "mysqldump --opt --user=${USERNAME} --password=${REMOTE_PASS} ${DBNAME} | gzip > ${DBFILE}" 

$RSYNC --rsh="$SSH -i /Users/zahra/.ssh/id_rsa" --progress --partial -avz ${LOCAL_SENSORS_DIR} ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_SENSORS_DIR}

$RSYNC --progress --partial -avz ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_DB_DIR} ${LOCAL_DB_DIR} 

