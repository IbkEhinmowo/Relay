from Core.Integrations.Schedular import (
    add_periodic_task,
    add_cron_task as _add_cron_task,
    remove_task as _remove_task,
    list_tasks as _list_tasks,
    remove_all_tasks as _remove_all_tasks,
)

def add_task(name, task, interval_seconds, arg):
    add_periodic_task.delay(name, task, interval_seconds, arg)
    print(f"Sent request to add task: {name}")
    
    
    
# --- NEW FUNCTION ---
def add_cron_task(name, task, arg, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'):
    _add_cron_task.delay(name, task, arg, minute, hour, day_of_week, day_of_month, month_of_year)
    print(f"Sent request to add CRON task: {name}")


def remove_task(name):
    _remove_task.delay(name)
    print(f"Sent request to remove task: {name}")


# --- NEW FUNCTION ---
def list_tasks():
    print("Listing scheduled tasks...")
    tasks = _list_tasks()
    print("Scheduled tasks:")
    for task in tasks:
        print(task)


# --- NEW FUNCTION ---
def remove_all_tasks():
    result = _remove_all_tasks.delay()
    print("Sent request to remove all tasks. Waiting for result...")
    message = result.get(timeout=30)
    print(message)


if __name__ == '__main__':
   list_tasks()
   remove_all_tasks()

    # Add a new task by sending a request to the running Celery worker
    # add_task(
    #     name='dynamic-task-2', 
    #     task='Core.Integrations.Schedular.test', 
    #     interval_seconds=10, 
    #     arg='I am dynamic and it works!'
    # )
    
    
    # remove_task('dynamic-task-2')
    # list_tasks()