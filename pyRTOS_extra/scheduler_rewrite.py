import pyRTOS


def time_scheduler(tasks):
    messages = []
    running_task = None

    for task in tasks:
        if task.state == pyRTOS.BLOCKED:
            if True in map(lambda x: next(x), task.ready_conditions):
                task.state = pyRTOS.READY
                task.ready_conditions = []

        if task.state == pyRTOS.READY or task.state == pyRTOS.RUNNING:
            if running_task == None:
                running_task = task
            elif running_task.priority > task.priority:
                running_task = task
			elif task.state == pyRTOS.RUNNING:
				running_task = task

    if running_task:
        running_task.state = pyRTOS.RUNNING

        try:
            messages = running_task.run_next()
        except StopIteration:
            tasks.remove(running_task)
    
    return messages
