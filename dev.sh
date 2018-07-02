python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:8000
sleep 10
celery -A AnalysisSite worker -B -l info
