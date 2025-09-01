from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


# The first argument is the name of the current module, which is named 'Schedular'
# The broker argument specifies the url of the message broker (Redis in tis case)
# The redbeat_redis_url is for the RedBeat scheduler
app = Celery('Schedular', 
             broker='redis://localhost:6379/5',
             backend='redis://localhost:6379/7',
             redbeat_redis_url='redis://localhost:6379/6',
             include=['Core.Processor.LLMAGENT'])

# Tell Celery to use the RedBeat scheduler
app.autodiscover_tasks(packages=['Core.Processor'], related_name='tasks')

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
def add_cron_task(name, task, arg, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*', one_off=False):
    """
    Add a cron-style periodic task to RedBeat from a worker process.
    Can be set to run once and then be deleted.
    """
    from redbeat import RedBeatSchedulerEntry

    task_to_schedule = task
    args_for_task = [arg]

    if one_off:
        task_to_schedule = 'Core.Integrations.Schedular.run_once_and_remove'
        args_for_task = [name, task, arg]

    entry = RedBeatSchedulerEntry(
        name=name,
        task=task_to_schedule,
        schedule=crontab(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
        ),
        args=args_for_task,
        app=app
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


@app.task
def run_once_and_remove(name, task, arg):
    """
    Executes a task and then removes itself from the schedule.
    """
    # Run the original task by name
    app.send_task(task, args=[arg])
    # Remove the cron job that triggered this
    remove_task.delay(name)
    print(f"Task {name} executed once and is being removed.")


@app.task
def remove_all_tasks():
    """
    Remove all scheduled RedBeat periodic tasks.
    """
    from redbeat import RedBeatScheduler, RedBeatSchedulerEntry
    scheduler = RedBeatScheduler(app=app)
    # Get all task keys from Redis
    keys = scheduler.app.backend.client.keys('redbeat:*')
    count = 0
    for key in keys:
        try:
            # Decode key to string
            key_str = key.decode('utf-8')
            # Extract task name from key
            name = key_str.split('redbeat:')[1]
            if ':' in name: # Avoid deleting internal redbeat keys
                continue
            entry = RedBeatSchedulerEntry.from_key(key_str, app=app)
            entry.delete()
            print(f"Removed task: {name}")
            count += 1
        except Exception as e:
            print(f"Error removing task from key {key}: {e}")
    print(f"Removed {count} tasks.")
    return f"Removed {count} tasks."


# List all scheduled RedBeat tasks
def list_tasks():
    """
    List all scheduled RedBeat periodic tasks.
    """
    from redbeat import RedBeatScheduler
    scheduler = RedBeatScheduler(app=app)
    entries = scheduler.schedule
    task_list = []
    for name, entry in entries.items():
        task_list.append({
            'name': name,
            'task': entry.task,
            'schedule': str(entry.schedule),
            'args': entry.args,
            'kwargs': entry.kwargs,
        })
    print("Scheduled tasks:", task_list)
    return task_list



# To run the worker:
# celery -A Core.Integrations.Schedular worker --loglevel=info

# To run the beat scheduler (it now uses RedBeat):
# celery -A Core.Integrations.Schedular beat -S redbeat.RedBeatScheduler --loglevel=info
