import bson.objectid as object_id
from django.shortcuts import redirect

from dashboard import models

# Create your views here.
def task_control(request, id):
    task = models.Task.objects.filter(_id=object_id.ObjectId(id)).first()
    if task and not task.is_running():
        task.start()
    else:
        print("Task not found")
    return redirect('/admin/dashboard/task/')
