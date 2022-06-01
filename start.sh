#!/bin/sh

#
#	Copy this file to /home in azure container
#	Point this file as custom script to be executed
#


/opt/startup/startup.sh&
disown

# Add your custom command here
echo "0 0 * * * source $VIRTUALENVIRONMENT_PATH/bin/activate && python $APP_PATH/manage.py runcrons > /home/cron_task.log" | crontab