python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:8000
celery -A AnalysisSite worker -B -l info
