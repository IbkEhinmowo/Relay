from redbeat import RedBeatScheduler
from celery.schedules import schedule, crontab
from Core.Integrations.Schedular import app

# Create a scheduler instance
scheduler = RedBeatScheduler(app=app)

def add_task(name, task, interval_seconds, arg):
    """
    Adds a new periodic task to the RedBeat schedule.
    """
    entry = scheduler.Entry(
        name=name,
        task=task,
        schedule=schedule(run_every=interval_seconds),
        args=[arg]
    )
    scheduler.add(entry)
    print(f"Added task: {name}")

def remove_task(name):
    """
    Removes a periodic task from the RedBeat schedule.
    """
    scheduler.remove(name)
    print(f"Removed task: {name}")

def list_tasks():
    """
    Lists all tasks in the schedule.
    """
    print("Current scheduled tasks:")
    for key in scheduler.get_all_keys():
        entry = scheduler.get_entry_from_key(key)
        print(f"- {entry.name}: runs every {entry.schedule.run_every} seconds")


if __name__ == '__main__':
    # --- Example Usage ---

    # Clear the schedule first for a clean slate
    # for key in scheduler.get_all_keys():
    #     scheduler.remove(scheduler.get_entry_from_key(key).name)

    # Add a new task
    add_task(
        name='dynamic-task-1', 
        task='Core.Integrations.Schedular.test', 
        interval_seconds=10, 
        arg='I am dynamic!'
    )

    # Add another task
    add_task(
        name='another-dynamic-task',
        task='Core.Integrations.Schedular.test',
        interval_seconds=30,
        arg='So am I!'
    )

    # List all current tasks
    list_tasks()

    # Example of how to remove a task (uncomment to try)
    # remove_task('dynamic-task-1')
    # list_tasks()
