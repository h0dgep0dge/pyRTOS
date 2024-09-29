import pyRTOS

def increment_scheduler(tasks):
    messages = []
    running_task = None

    for task in tasks:
        if not hasattr(task,"subPriority"):
            task.subPriority = 0
        
        if task.state == pyRTOS.BLOCKED:
            if True in map(lambda x: next(x), task.ready_conditions):
                task.state = pyRTOS.READY
                task.ready_conditions = []

        if task.state == pyRTOS.READY or task.state == pyRTOS.RUNNING:
            if running_task == None:
                running_task = task
            elif running_task.priority > task.priority:
                running_task = task
            elif task.priority == running_task.priority:
                if task.subPriority > running_task.subPriority:
                    running_task = task
                elif task.subPriority == running_task.subPriority:
                    task.subPriority += 1

    if running_task:
        running_task.state = pyRTOS.RUNNING
        running_task.subPriority = 0

        try:
            messages = running_task.run_next()
        except StopIteration:
            tasks.remove(running_task)
    
    return messages