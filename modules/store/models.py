from django.db import models
from common.exception import ApiError
from common.export import XlsxExportConfig, XlsxExportField
from common.models import Model
from common.wrapped import jsonGetter

# Create your models here.
class ProductCategory(Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="category", blank=True, null=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)

    xlsx_config:XlsxExportConfig = XlsxExportConfig(
        fields=[
            XlsxExportField(prop="id",label="ID"),
            XlsxExportField(prop="name",label="名称"),
            XlsxExportField(prop="description",label="描述"),
            XlsxExportField(prop="icon",label="图片",type="image"),
        ]
    )
    def __str__(self):
        return self.name
    
    @jsonGetter(name="children")
    def children(self):
        return ProductCategory.objects.filter(parent=self)
    
    @jsonGetter(name="parent_id")
    def get_parent_id(self):
        return f"{self.parent.id}" if self.parent else None
    
    def save(self, *args, **kwargs):
        parent_id = getattr(self, 'parent_id', None)
        print("parent_id:",self)
        parent = None
        if parent_id:
            parent = ProductCategory.objects.filter(id=parent_id).first()
        else:
            self.parent = None
        if parent:
            if parent == self:
                raise ApiError('分类不能是自己的子分类')
            if parent.parent is not None:
                raise ApiError('仅能有一级分类')
            if self.id:
                children = ProductCategory.objects.filter(parent_id = self.id)
                if len(children) > 0:
                    raise ApiError('仅能有一级分类')
        super().save(*args, **kwargs)
    
# brand 
class ProductBrand(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True)
    enable = models.BooleanField(default=True)
    link = models.TextField(blank=True)

    xlsx_config = XlsxExportConfig(
        fields=[
            XlsxExportField(prop="id",label="ID"),
            XlsxExportField(prop="name",label="名称"),
            XlsxExportField(prop="description",label="描述"),
            XlsxExportField(prop="icon",label="图片",type="image"),
        ]
    )

    def __str__(self):
        return self.name
    
# tag 
class ProductTag(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# services 
class ProductService(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# sku_group 
class ProductAttrGroup(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# 属性用来筛选和展示，暂时不和 sku 绑定
# 比如 sku 一般是 内存:2G，颜色:红色, 属性是 内存:闪迪，屏幕尺寸:4K 屏幕供应商:三星,等一些其他信息，仅用来暂时或者筛选 
class ProductAttr(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.ForeignKey(ProductAttrGroup, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name
    
    @jsonGetter(name="group_name")
    def group_name(self):
        return self.group.name if self.group else None
    
    @jsonGetter(name="group_id")
    def get_group_id(self):
        return f"{self.group.id}" if self.group else None
    
class ProductAttrValue(Model):
    attr = models.ForeignKey(ProductAttr, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    @jsonGetter(name="attr_name")
    def attr_name(self):
        return self.attr.name
    
    @jsonGetter(name="attr_id")
    def get_attr_id(self):
        return f"{self.attr.id}"
    
#颜色
class ProductSku(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 红，绿，蓝
class ProductSkuValue(Model):
    sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    @jsonGetter(name="sku_name")
    def sku_name(self):
        return f"{self.sku.name}-{self.sku.description}"
    
class Product(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.TextField(blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, on_delete=models.DO_NOTHING)
    tag_ids = models.CharField(max_length=255)
    service_ids = models.CharField(max_length=255)



    def skus(self):
        return ProductSkuRelation.objects.filter(product=self)
    
    def attrs(self):
        return ProductAttrRelation.objects.filter(product=self)

    def __str__(self):
        return self.name


class ProductSkuRelation(Model):
    sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def sku_values(self):
        return ProductSkuValueRelation.objects.filter(sku=self.sku)

class ProductSkuValueRelation(Model):
    sku = models.ForeignKey(ProductSkuRelation, on_delete=models.CASCADE)
    sku_value = models.ForeignKey(ProductSkuValue, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()
    old_price = models.IntegerField()
    image = models.TextField(blank=True)

class ProductAttrRelation(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attr = models.ForeignKey(ProductAttr, on_delete=models.CASCADE)
    attr_value = models.ForeignKey(ProductAttrValue, on_delete=models.CASCADE)