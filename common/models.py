from django.db import models

from common.export import XlsxExportConfig

class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    hidden_fields = []
    protected_fields = ["id", "created_at", "updated_at"]
    xlsx_config:XlsxExportConfig = XlsxExportConfig([])

    class Meta:
        abstract = True
