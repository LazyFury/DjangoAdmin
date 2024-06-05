from django.db import models

from common.exception import ApiError
from common.export import XlsxExportConfig, XlsxExportField
from common.models import Model
from common.wrapped import jsonGetter

# Create your models here.
class ArticleTag(Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag
    
    @jsonGetter(name='name')
    def name(self):
        return self.tag
    
class ArticleCategory(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)


    xlsx_config:XlsxExportConfig = XlsxExportConfig(
        fields=[
            XlsxExportField(prop='name', label='名称'),
            XlsxExportField(prop='description', label='描述'),
            XlsxExportField(prop='parent_name', label='父分类'),
        ]
    )
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_children(category):
        children = ArticleCategory.objects.filter(parent=category)
        if not children:
            return []
        return children + ArticleCategory.get_all_children(children)
    
    @jsonGetter(name='parent_name')
    def parent_name(self):
        return self.parent.name if self.parent else None
    
    @jsonGetter(name='parent_id')
    def parent__id(self):
        return f"{self.parent.id}" if self.parent else None
    
    @jsonGetter(name='children')
    def children(self):
        return ArticleCategory.objects.filter(parent=self)
    
    def all_children(self):
        return ArticleCategory.get_all_children(self)
    
    def has_children(self):
        return len(self.all_children()) > 0
    
    def delete(self, *args, **kwargs):
        if self.has_children():
            raise ApiError('This category has children, please delete them first')
        super().delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        
        parent_id = getattr(self, 'parent_id', None)
        if parent_id:
            parent = ArticleCategory.objects.filter(id=parent_id).first()
            if parent and parent == self:
                raise ApiError('分类不能是自己的子分类')
            valid_parent = parent
            while True:
                if not valid_parent:
                    break
                if valid_parent == self:
                    raise ApiError('顶级分类不能是自己的子分类')
                valid_parent = valid_parent.parent
        super().save(*args, **kwargs)


    
class Article(Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag_ids = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')

    xlsx_config:XlsxExportConfig = XlsxExportConfig(
        fields=[
            XlsxExportField(prop='title', label='标题'),
            XlsxExportField(prop='description', label='描述'),
            XlsxExportField(prop='content', label='内容'),
            XlsxExportField(prop='is_published', label='是否发布'),
            XlsxExportField(prop='author_name', label='作者'),
            XlsxExportField(prop='category_name', label='分类'),
            XlsxExportField(prop='tag_names_join', label='标签'),
        ]
    )

    def __str__(self):
        return self.title
    
    @jsonGetter(name='author_name')
    def author_name(self):
        return self.author.username
    
    @jsonGetter(name='author_id')
    def author__id(self):
        return f"{self.author.id}"
    
    @jsonGetter(name='author_avatar')
    def author_avatar(self):
        return self.author.avatar.url if self.author.avatar else None
    
    @jsonGetter(name='category_name')
    def category_name(self):
        return self.category.name
    
    @jsonGetter(name='category_id')
    def category__id(self):
        return f"{self.category.id}"
    
    @jsonGetter(name='tag_ids')
    def get_tag_ids(self):
        return self.tag_ids.split(',') if self.tag_ids else []
    
    @jsonGetter(name='tag_names')
    def get_tag_names(self):
        return [tag.tag for tag in ArticleTag.objects.filter(id__in=self.get_tag_ids(self))]
    
    @jsonGetter(name='tag_names_join')
    def get_tag_names_join(self):
        return ','.join(self.get_tag_names(self))

    def get_content_desc_without_html(self, length=100):
        import re
        return re.sub(r'<[^>]+>', '', self.content[:length])

    @jsonGetter(name="description")
    def get_description(self):
        return self.description if self.description else self.get_content_desc_without_html(100) or 'No description'

    
    def save(self, *args, **kwargs):
        if self.tag_ids and isinstance(self.tag_ids, list):
            self.tag_ids = ",".join(self.tag_ids)
        super().save(*args, **kwargs)
