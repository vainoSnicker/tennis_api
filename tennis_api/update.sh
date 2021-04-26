#! /bin/sh.
sudo docker exec -ti tennis_api_web_1 sh -c "python manage.py update_data"
