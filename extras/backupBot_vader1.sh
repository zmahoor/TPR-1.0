#!/bin/bash
RSYNC=/usr/bin/rsync
SSH=/usr/bin/ssh
#-------------------------To be set by user-------------------------------------
REMOTE_HOST="45.79.171.136"
REMOTE_USERNAME="root"

LOCAL_MAIN_DIR="/Users/zahra/TPR"
REMOTE_MAIN_DIR="/backup_tpr"
#-------------------------------------------------------------------------------
#path to the sensor from the last hour
TEMP_PATH="$(date -v -1H '+%Y/%m/%d/%H')"

LOCAL_SENSORS_DIR="$LOCAL_MAIN_DIR/sensors/$TEMP_PATH/"
LOCAL_CONTROLLERS_DIR="$LOCAL_MAIN_DIR/controllers/$TEMP_PATH/"
LOCAL_DB_DIR="$LOCAL_MAIN_DIR/db"

REMOTE_SENSORS_DIR="$REMOTE_MAIN_DIR/sensors/$TEMP_PATH"
REMOTE_CONTROLLERS_DIR="$REMOTE_MAIN_DIR/controllers/$TEMP_PATH"
REMOTE_DB_DIR="$REMOTE_MAIN_DIR/db/"

echo $REMOTE_SENSORS_DIR
echo $LOCAL_SENSORS_DIR

find "$LOCAL_MAIN_DIR/db/" -name "*.sql.gz" -mtime +0 -print -delete

#send the sensors produced in the previous hour to the cloud
$SSH ${REMOTE_USERNAME}@${REMOTE_HOST} "mkdir -p $REMOTE_SENSORS_DIR" && 
$RSYNC --progress --partial -avz ${LOCAL_SENSORS_DIR} ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_SENSORS_DIR}

#send the controllers produced in the previous hour to the cloud
$SSH ${REMOTE_USERNAME}@${REMOTE_HOST} "mkdir -p $REMOTE_CONTROLLERS_DIR" && 
$RSYNC --progress --partial -avz ${LOCAL_CONTROLLERS_DIR} ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_CONTROLLERS_DIR}

#store the most recent backup of the database from the cloud
$RSYNC --progress --partial -avz ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_DB_DIR} ${LOCAL_DB_DIR} 

# SENSOR_FILE="s$(date -v -1H '+%Y%m%d%H').tar.gz"

# tar -czvf ${COMPRESSED_FILE} -C $LOCAL_SENSORS_DIR .
# ssh ${REMOTE_USERNAME}@${REMOTE_HOST} "mkdir -p $REMOTE_SENSORS_DIR" && scp ${SENSOR_FILE} ${REMOTE_USERNAME}@${REMOTE_HOST}:${REMOTE_SENSORS_DIR}
# rm  ${SENSOR_FILE}

# ssh ${REMOTE_USERNAME}@${REMOTE_HOST} "mysqldump --opt --user=${USERNAME} --password=${REMOTE_PASS} ${DBNAME} | gzip > ${DBFILE}" 

# PREV_YEAR="$(date -v -1H '+%Y')"
# PREV_MONTH="$(date -v -1H '+%m')"
# PREV_DAY="$(date -v -1H '+%d')"
# PREV_HOUR="$(date -v -1H '+%H')"

