from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    plan = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)
            
    




