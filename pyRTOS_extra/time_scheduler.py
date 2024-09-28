import pyRTOS
import time

def time_scheduler(tasks):
    messages = []
    running_task = None
    for task in tasks:
        if not hasattr(task,"lastRun"):
            task.lastRun = 0
        
        if task.state == pyRTOS.BLOCKED:
            if True in map(lambda x: next(x), task.ready_conditions):
                task.state = pyRTOS.READY
                task.ready_conditions = []

        if task.state == pyRTOS.READY or task.state == pyRTOS.RUNNING:
            if running_task == None:
                running_task = task
            elif running_task.priority > task.priority:
                running_task = task
            elif running_task.priority == task.priority and running_task.lastRun > task.lastRun:
                running_task = task

    if running_task:
        running_task.state = pyRTOS.RUNNING
        running_task.lastRun = time.monotonic()

        try:
            messages = running_task.run_next()
        except StopIteration:
            tasks.remove(running_task)
    
    return messages
