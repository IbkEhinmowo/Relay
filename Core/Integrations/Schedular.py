from celery import Celery
from celery.schedules import crontab


# The first argument is the name of the current module, which is named 'Schedular'
# The broker argument specifies the url of the message broker (Redis in tis case)
# The redbeat_redis_url is for the RedBeat scheduler
app = Celery('Schedular', 
             broker='redis://localhost:6379/5',
             redbeat_redis_url='redis://localhost:6379/6')

# Tell Celery to use the RedBeat scheduler
app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'


@app.task
def test(a):
    """
    A simple test task that prints the argument.
    """
    a = "Task executed with argument: " + a
    print(a)

# To run the worker:
# celery -A Core.Integrations.Schedular worker --loglevel=info

# To run the beat scheduler (it now uses RedBeat):
# celery -A Core.Integrations.Schedular beat -S redbeat.RedBeatScheduler --loglevel=info
