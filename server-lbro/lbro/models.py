from django.db import models

class Query(models.Model):
    class Meta:
        db_table = 'lbro_query'

    query = models.CharField(max_length=200)

    def __str__(self):
        return self.query

class Article(models.Model):
    class Meta:
        db_table = 'lbro_article'

    query = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    authors = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=25, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    fulldoc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserDefault(models.Model):
    class Meta:
        db_table = 'lbro_user'
    
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, null=True, blank=True, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username
