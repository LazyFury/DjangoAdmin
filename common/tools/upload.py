

import datetime
from hashlib import md5
import os
import random

from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile

from app import settings
from common.response import ApiJsonResponse

def check_file_type(file:UploadedFile):
    return file.content_type in settings.ALLOW_FILE_TYPE

def check_file_size(file:UploadedFile):
    return file.size <= settings.MAX_FILE_SIZE

def upload_handler(request:HttpRequest):
    file = request.FILES.get("file")
    if not file:
        raise ValueError("file is required")
    uploaded_file = upload_file(file)
    return ApiJsonResponse.success(uploaded_file)

def upload_image_handler(request:HttpRequest):
    file = request.FILES.get("file")
    if not file:
        raise ValueError("file is required")
    if file.content_type not in settings.ALLOW_IMAGE_TYPE:
        raise ValueError("文件类型不允许")
    uploaded_file = upload_file(file, "temp/upload/image")
    return ApiJsonResponse.success(uploaded_file)

def upload_video_handler(request:HttpRequest):
    file = request.FILES.get("file")
    if not file:
        raise ValueError("file is required")
    if file.content_type not in settings.ALLOW_VIDEO_TYPE:
        raise ValueError("文件类型不允许")
    uploaded_file = upload_file(file, "temp/upload/video")
    return ApiJsonResponse.success(uploaded_file)

def upload_file(file:UploadedFile, path="temp/upload", name=None):
    if not name:
        name = file.name
    real_path = os.path.join(settings.BASE_DIR, path)
    file_suffix = name.split(".")[-1]
    time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 文件名 md5 不可用做文件的唯一表示，避免文件名重复 / 读文件进行 md5 好像没太大必要暂时不做
    name = md5(name.encode("utf-8")).hexdigest() + "_" + time_str + "." + file_suffix
    
    if not check_file_type(file):
        raise ValueError("文件类型不允许")
    if not check_file_size(file):
        raise ValueError("文件大小超出限制")

    if not os.path.exists(real_path):
        os.makedirs(real_path)

    if os.path.exists(os.path.join(real_path, name)):
        name += randome_str()

    with open(os.path.join(real_path, name), 'wb') as f:
        f.write(file.read())
    return path + "/" + name

def randome_str(length=8):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    return "".join(sa)
