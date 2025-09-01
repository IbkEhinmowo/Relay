from celery import Celery
from celery.schedules import crontab

# Create a Celery instance
# The first argument is the name of the current module, which is 'Schedular'
# The broker argument specifies the URL of the message broker (Redis)
app = Celery('Schedular', broker='redis://localhost:6379/5')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Set up periodic tasks for Celery Beat.
    This function is called after Celery is configured.
    """
    # Add a task to run every minute
    sender.add_periodic_task(60.0, test.s('Hello'), name='add every 60')

    # Add a task to run every day at 8:00 AM
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        test.s('Good morning!'),
    )

@app.task
def test(arg):
    """
    A simple test task that prints the argument.
    """
    print(arg)

# To run the worker:
# celery -A Core.Integrations.Schedular worker --loglevel=info

# To run the beat scheduler:
# celery -A Core.Integrations.Schedular beat --loglevel=info
