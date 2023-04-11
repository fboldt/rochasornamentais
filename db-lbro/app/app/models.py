from django.db import models



class Article(models.Model):
    class Meta:
        db_table = 'lbro_article'
    
    title = models.CharField(max_length=200,null=True,blank=True)
    link = models.URLField(max_length=200,null=True,blank=True)
    authors = models.CharField(max_length=200,null=True,blank=True)
    year = models.CharField(max_length=25,null=True,blank=True)
    abstract = models.TextField(null=True,blank=True)
    docId = models.CharField(max_length=200,null=True,blank=True)
    text = models.TextField(null=True,blank=True)

    

    def __str__(self):
        return self.title


class Query(models.Model):
    class Meta:
        db_table = 'lbro_queries'

    query = models.CharField(max_length=200,null=True,blank=True)
    date = models.FloatField(null=True,blank=True)
    user = models.CharField(max_length=200, null=True, blank=True)
    # articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.query

