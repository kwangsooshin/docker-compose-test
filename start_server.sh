nohup sh -- ./run_celery.sh > celery.log &
nohup sh -- ./run_django.sh > django.log &
echo "Start Server"
