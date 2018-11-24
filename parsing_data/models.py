from django.db import models

# Create your models here.
class ParsingData(models.Model):
    title = models.CharField(max_length = 200) # 제목
    abstract = models.CharField(max_length = 1000) # 초록         
    link = models.URLField() # Link
    created_at = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True) # 해당 레코드 갱신시 현재 시간 자동저장
    author = models.CharField(max_length = 100) # 저자
    content = models.TextField() # 내용