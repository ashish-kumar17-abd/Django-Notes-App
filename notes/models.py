from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)  # 📌 NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
