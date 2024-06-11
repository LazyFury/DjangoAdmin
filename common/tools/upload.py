

from hashlib import md5
import os

from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile

from app import settings
from common.response import ApiJsonResponse

def check_file_type(file:UploadedFile):
    return file.content_type in settings.ALLOW_FILE_TYPE

def upload_handler(request:HttpRequest):
    file = request.FILES.get("file")
    if not file:
        raise ValueError("file is required")
    uploaded_file = upload_file(file)
    return ApiJsonResponse.success(uploaded_file)

def upload_file(file:UploadedFile, path="temp/upload", name=None):
    if not name:
        name = file.name
    real_path = os.path.join(settings.BASE_DIR, path)
    file_suffix = name.split(".")[-1]
    name = md5(name.encode("utf-8")).hexdigest() + "." + file_suffix
    
    if not check_file_type(file):
        raise ValueError("文件类型不允许")

    if not os.path.exists(real_path):
        os.makedirs(real_path)

    with open(os.path.join(real_path, name), 'wb') as f:
        f.write(file.read())
    return path + "/" + name