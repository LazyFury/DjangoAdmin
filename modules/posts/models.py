from django.db import models

from common.exception import ApiError
from common.models import Model

# Create your models here.
class ArticleTag(Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag
    
class ArticleCategory(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_children(category):
        children = ArticleCategory.objects.filter(parent=category)
        if not children:
            return []
        return children + ArticleCategory.get_all_children(children)
    
    def all_children(self):
        return ArticleCategory.get_all_children(self)
    
    def has_children(self):
        return len(self.all_children()) > 0
    
    def delete(self, *args, **kwargs):
        if self.has_children():
            raise ApiError('This category has children, please delete them first')
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.parent and self.parent == self:
            raise ApiError('Parent category can not be self')
        for category in self.all_children():
            if category == self.parent:
                raise ApiError('Parent category can not be children')
        super().save(*args, **kwargs)


    
class Article(Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ArticleTag, related_name='articles')
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title
    
