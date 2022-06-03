#!/bin/sh
LOG_FILE=/home/needle/timer_update.log

if [[ -z "${UPDATE_TIME}" ]];then
	echo "No variable \$UPDATE_TIME defined. Using default 1 day timing" > $LOG_FILE
	UPDATE_TIME=$((( 24 * 60 * 60 )))
fi

# $APP_PATH is exported as environment variable duirng deployment
. $APP_PATH/antenv/bin/activate

while true;
do
	# Fetch the job hash and apply timer
	for i in $(python $APP_PATH/manage.py crontab show | awk 'NR>1 {print $1}');
	do
		echo "$(date): Commencing database update for $(python $APP_PATH/manage.py crontab show | grep $i)" > $LOG_FILE
		python $APP_PATH/manage.py crontab run $i
	done
	sleep $UPDATE_TIME
done&
disown