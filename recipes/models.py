from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# included created_by field to help with getting if author = can edit to work
# Thanks to Alex M for pointing out I made a mistake of passing in Author
# instead of User into created_by

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', null=True, default=None)
    description = models.TextField()
    instructions = models.TextField()
    time_required = models.CharField(max_length=50)
    favorite = models.ManyToManyField(User, related_name='like')

    def __str__(self):
        return self.title
