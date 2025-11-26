from django.db import models
from api.models import User
from django.utils import timezone
class Category(models.Model):
    name = models.CharField(max_length=102, unique=True)

    def __str__(self):
        return self.name
    
    
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time


    def __str__(self):
        return f"{self.title} | {self.user.username}"
    


    

