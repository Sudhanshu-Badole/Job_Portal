from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    #category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
