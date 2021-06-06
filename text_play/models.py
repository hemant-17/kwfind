from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Keyword(models.Model):
    keyword = models.CharField(max_length=200,primary_key=True)

    def __str__(self):
        return self.keyword

class Url(models.Model):
    id=models.AutoField(primary_key=True)
    url=models.URLField(max_length=2090,unique=True)

    def __str__(self):
        return self.url


class Mapping_of_url(models.Model):
    url_id=models.ForeignKey(to=Url,on_delete=models.CASCADE)
    keyword=models.ForeignKey(to=Keyword,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url_id} {self.keyword}"
