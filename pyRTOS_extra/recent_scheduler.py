import pyRTOS

exec_history = []

def recent_scheduler(tasks):
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
            elif running_task.priority == task.priority:
                try:
                    task_index = exec_history.index(id(task))
                    task_in = True
                except ValueError:
                    task_in = False

                try:
                    running_task_index = exec_history.index(id(task))
                    running_task_in = True
                except ValueError:
                    running_task_in = False
                    
                if running_task_in and task_in and task_index < running_task_index:
                    running_task = task
                elif running_task_in and not task_in:
                    running_task = task

    if running_task:
        running_task.state = pyRTOS.RUNNING

        if id(running_task) in exec_history:
            exec_history.remove(id(running_task))
        exec_history.append(id(running_task))

        try:
            messages = running_task.run_next()
        except StopIteration:
            tasks.remove(running_task)
            exec_history.remove(id(running_task))
    
    return messages
