apt-get update -y
apt-get install cron
python manage.py crontab add
service cron start

python manage.py runserver 80