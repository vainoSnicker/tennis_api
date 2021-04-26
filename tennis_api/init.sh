#! /bin/sh.
sudo docker exec -ti tennis_api_web_1 sh -c "python manage.py migrate | python manage.py init_data -s $1"
