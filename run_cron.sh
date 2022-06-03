#!/bin/sh

sleep_time=$((( 24 * 60 * 60 )))

# $APP_PATH is exported as environment variable duirng deployment
. $APP_PATH/antenv/bin/activate

while true;
do
	# Fetch the job hash and apply timer
	for i in $(python $APP_PATH/manage.py crontab show | awk 'NR>1 {print $1}');
	do
		echo "$(date): Commencing database update for $(python $APP_PATH/manage.py crontab show | grep $i)" > /home/timer_update.log
		python $APP_PATH/manage.py crontab run $i
	done
	sleep $sleep_time
done&
disown