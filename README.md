#Dmonitor
the monitor system for Docker.
#running env
ubuntu 16.04
python 2.7
django

#Start Server
cd /Dmonitor
python manage.py runserver 0.0.0.0:8000

#Start Agent
cd /agent
python agent.py start

