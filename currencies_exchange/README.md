Creating rabbitmq user
rabbitmqctl add_user test test
rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

Run celery worker:
celery -A tasks worker --loglevel=info

Run celery pereodic task:
celery -A tasks beat --loglevel=info 


Reread supervisor config:
supervisorctl reread
supervisorctl update
