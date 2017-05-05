#!/bin/bash
#-------------------------To be set by user-------------------------------------
MAINDIR="/backup_tpr"
USERNAME="root"
DBNAME="TwitchPlays"
PASS="twitchplaysrobotics2138"
#-------------------------------------------------------------------------------

DBFILE="$MAINDIR/db/db$(date +'%Y%m%d%H').sql.gz"
echo $DBFILE

find "$MAINDIR/db" -name "*.sql.gz" -mtime +1 -print -delete

mysqldump --opt --user=${USERNAME} --password=${PASS} ${DBNAME} | gzip > ${DBFILE}  



