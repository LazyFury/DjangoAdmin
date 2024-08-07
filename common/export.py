

import datetime

from app import settings


class ExportConfig(object):
    def __init__(self,**kwargs) -> None:
        self.config = {}
        self.config.update(**kwargs)

class XlsxExportField(object):
    BOOL_FORMAT_STYLE = "是,否"
    DATE_FORMAT_STYLE = "%Y-%m-%d %H:%M:%S"

    def __init__(self,prop:str,label:str,type:str="",formater:str="",sort:int=0,sum:bool = False) -> None:  # noqa: A002
        """
        Initializes a new instance of the XlsxExportField class.

        Args:
            prop (str): The property name.
            label (str): The label for the property.
            type (str, optional): The type of the property. Defaults to "".
            formater (str, optional): The formatter for the property. Defaults to "".
            sort (int, optional): The sort order of the property. Defaults to 0.
            sum (bool, optional): Whether the property is a sum. Defaults to False.
        """
        self.prop = prop
        self.label = label
        self.type = type # deprecated
        self.formater = formater
        self.sort = sort
        self.sum = sum

    def format(self,value):
        """
        Formats the given value based on its type.

        Args:
            value (Any): The value to be formatted.

        Returns:
            Union[str, datetime.datetime]: The formatted value.

        If the value is an instance of datetime.datetime, it is formatted using the formatter specified in the `formater` attribute.
        If the value is an instance of bool, it is formatted based on the formatter specified in the `formater` attribute.
        If the value is of type 'image', it is formatted by appending it to the `work_path` specified in the `settings.BASE_DIR` attribute.
        If none of the above conditions are met, the value is returned as is. If the value is None, '/' is returned.
        """
        print("xlsx format:",self.type,value)

        if isinstance(value,datetime.datetime):
            if self.formater == "":
                self.formater = self.DATE_FORMAT_STYLE
            return value.strftime(self.formater)
        if isinstance(value,bool):
            if self.formater == "":
                self.formater = self.BOOL_FORMAT_STYLE
            TrueValue,FalseValue = self.formater.split(",")  # noqa: N806
            return TrueValue if value else FalseValue
        if self.type == 'image':
            work_path = settings.BASE_DIR
            if value.startswith("http"):
                return value
            if value.startswith("/"):
                return f"{work_path}{value}"
            else:
                return f"{work_path}/{value}"
            
        return value or "/"


class XlsxExportConfig(ExportConfig):
    def __init__(self,fields:list[XlsxExportField],**kwargs) -> None:
        """
        Initializes a new instance of the XlsxExportConfig class.

        Args:
            fields (list[XlsxExportField]): A list of XlsxExportField objects representing the fields to be exported.
            **kwargs: Additional keyword arguments to be passed to the parent class constructor.

        Returns:
            None

        Initializes the `fields` attribute of the instance with the provided list of XlsxExportField objects.
        Calls the constructor of the parent class with the provided keyword arguments.
        """
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