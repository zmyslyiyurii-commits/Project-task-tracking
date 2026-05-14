from django.db import models
from django.contrib.auth.models import User

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_invites', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_invites', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    seconds_spent = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date') # Один запис на день для кожного юзера

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.seconds_spent}s"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) 
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# python manage.py runserver
# http://127.0.0.1:8000/admin/tracker/task/
# git add .
# git commit -m ""
# git push -u origin main