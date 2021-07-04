from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    load = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_likes(self):
        return self.likes.count()

    def get_comments(self):
        return self.comments.count()

    def get_load(self):
        if self.load * 5 > len(Blogs.objects.all()):
            self.load = 0
            return float("inf")
        else:
            self.load += 1
            return self.load


class BlogComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


class BlogLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)
