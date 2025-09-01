from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


# The first argument is the name of the current module, which is named 'Schedular'
# The broker argument specifies the url of the message broker (Redis in tis case)
# The redbeat_redis_url is for the RedBeat scheduler
app = Celery('Schedular', 
             broker='redis://localhost:6379/5',
             backend='redis://localhost:6379/7',
             redbeat_redis_url='redis://localhost:6379/6')

# Tell Celery to use the RedBeat scheduler

app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
app.conf.beat_max_loop_interval = 5  # Check for new tasks every 5 seconds
app.conf.timezone = 'UTC'
app.conf.enable_utc = True



@app.task
def add_periodic_task(name, task, interval_seconds, arg):
    """
    A task that adds another periodic task to the schedule.
    """
    from redbeat import RedBeatSchedulerEntry
    from celery.schedules import schedule
    entry = RedBeatSchedulerEntry(
        name=name,
        task=task,
        schedule=schedule(run_every=timedelta(seconds=int(interval_seconds))),
        args=[arg],
        app=app,
    )
    entry.save()
    print(f"Dynamically added task: {name}")


@app.task
def test(arg: str):
    """Simple demo task to verify periodic scheduling runs."""
    print(f"[test] ran with arg='{arg}'")


@app.task
def add_cron_task(name, task, arg, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'):
    """
    Add a cron-style periodic task to RedBeat from a worker process.
    """
    from redbeat import RedBeatSchedulerEntry
    entry = RedBeatSchedulerEntry(
        name=name,
        task=task,
        schedule=crontab(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
        ),
        args=[arg],
        app=app,
    )
    entry.save()
    print(f"Dynamically added CRON task: {name}")


@app.task
def remove_task(name):
    """
    Remove a RedBeat periodic task by its unique name.
    """
    from redbeat import RedBeatSchedulerEntry
    try:
        entry = RedBeatSchedulerEntry.from_key(f'redbeat:{name}', app=app)
        entry.delete()
        print(f"Removed task: {name}")
    except KeyError:
        print(f"Task {name} not found.")



# To run the worker:
# celery -A Core.Integrations.Schedular worker --loglevel=info

# To run the beat scheduler (it now uses RedBeat):
# celery -A Core.Integrations.Schedular beat -S redbeat.RedBeatScheduler --loglevel=info
