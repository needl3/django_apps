#!/bin/sh

# Copy all necessary steps defined from deployment
cat /opt/startup/startup.sh | head -n -1 > startup.sh

# Add your custom command here
echo '
apt-get update -y
apt-get install cron -y
python manage.py crontab add
service cron start' >> startup.sh

# Add last line that'll startup the server
cat /opt/startup/startup.sh | tail -n 1 >> startup.sh

chmod +x startup.sh

./startup.sh