

import datetime


class ExportConfig(object):
    def __init__(self,**kwargs) -> None:
        self.config = {}
        self.config.update(**kwargs)

class XlsxExportField(object):
    BOOL_FORMAT_STYLE = "是,否"
    DATE_FORMAT_STYLE = "%Y-%m-%d %H:%M:%S"

    def __init__(self,prop:str,label:str,type:str="",formater:str="",sort:int=0,sum:bool = False) -> None:
        self.prop = prop
        self.label = label
        self.type = type # deprecated
        self.formater = formater
        self.sort = sort
        self.sum = sum

    def format(self,value):
        print("xlsx format:",self.type,value)

        if isinstance(value,datetime.datetime):
            if self.formater == "":
                self.formater = self.DATE_FORMAT_STYLE
            return value.strftime(self.formater)
        if isinstance(value,bool):
            if self.formater == "":
                self.formater = self.BOOL_FORMAT_STYLE
            TrueValue,FalseValue = self.formater.split(",")
            return TrueValue if value else FalseValue
        return value or "/"


class XlsxExportConfig(ExportConfig):
    def __init__(self,fields:list[XlsxExportField],**kwargs) -> None:
        super().__init__(**kwargs)
        self.fields = fields

    def __add__(self,other):
        assert isinstance(other,(XlsxExportField,XlsxExportConfig)),"XlsxExportConfig can only add XlsxExportField or XlsxExportConfig"
        if isinstance(other,XlsxExportField):
            self.fields.append(other)
        if isinstance(other,XlsxExportConfig):
            self.fields.extend(other.fields)
        return self
    
    def __repr__(self):
        return f"XlsxExportConfig({self.fields})"