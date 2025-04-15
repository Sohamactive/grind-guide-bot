def calculate_daily_score(completed_list, task_list):
    #here it counts number of completed tasks
    completed_tasks = completed_list.count(True)
    total_tasks = len(task_list)

    if total_tasks == 0:
        return 0,0
    completion_rate=completed_tasks/total_tasks
    
    points=completion_rate*100
    return completed_tasks,points
