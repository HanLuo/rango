from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length = 128, unique= True)

    def __str__(self):
        return self.name


class Page(models.Model):

    # ForeignKey ：用于建立一对多关系。
    # OneToOneField ：用于建立一对一关系。
    # ManyToManyField ：用于建立多对多关系。
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return self.title