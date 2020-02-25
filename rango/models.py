from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique = True)
    views = models.IntegerField(default=0) # exercise question
    likes = models.IntegerField(default=0) # exercise question
    def __str__(self): #for debugging
        return self.name 

    class Meta:
        verbose_name_plural = "Categories" # for fixing 'Categorys'

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self): # for debugging
        return self.title

