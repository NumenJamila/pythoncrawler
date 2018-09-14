from apscheduler.schedulers.blocking import BlockingScheduler
from .views import input
sched = BlockingScheduler() 
@sched.scheduled_job('interval', seconds=10)
def mytask(): 
    print("你好")
sched.start()