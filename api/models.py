from django.db import models
# from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    # author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    author = models.CharField(max_length=225)
    image = models.ImageField(upload_to='cumandra/images/')
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    # Sort post data in decending order
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + ' | ' + self.author
