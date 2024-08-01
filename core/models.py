import re
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest
from django.utils import timezone

from common.export import XlsxExportConfig, XlsxExportField
from common.models import Model
from common.wrapped import jsonGetter


class User(AbstractUser, Model):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    xlsx_config = XlsxExportConfig(
        fields=[
            XlsxExportField("id", "ID"),
            XlsxExportField("username", "用户名"),
            XlsxExportField("email", "邮箱"),
            XlsxExportField("nickname", "昵称"),
            XlsxExportField("bio", "简介"),
            XlsxExportField("birth_date", "生日", "date"),
            XlsxExportField("location", "位置"),
            XlsxExportField("longitude", "经度"),
            XlsxExportField("latitude", "纬度"),
            XlsxExportField("created_at", "创建时间", "date"),
            XlsxExportField("updated_at", "更新时间", "date"),
            XlsxExportField("is_active", "是否激活", "bool",sum=True),
            XlsxExportField("is_staff", "是否员工", "bool",sum=True),
            XlsxExportField("is_superuser", "是否超级用户", "bool"),
            XlsxExportField("first_name", "名"),
        ]
    )

    protected_fields = ["password", "groups", "user_permissions", "last_login", "is_superuser"]

    @jsonGetter(name="avatar_url")
    def avatar_url(self):
        return self.avatar.url if self.avatar else None

    def get_all_permissions(self):
        groups = self.groups.all()
        group_permissions = [
            permission for group in groups for permission in group.permissions.all()
        ]
        user_permissions = self.user_permissions.all()
        permission = set()
        for p in group_permissions + list(user_permissions):
            permission.add(p)
        return permission


class UserToken(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    token = models.CharField(max_length=320, null=False, blank=False, unique=True)
    expire_at = models.DateTimeField(null=True)

    user_agent = models.CharField(max_length=255, null=True, blank=True)
    sec_ua = models.TextField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    platform = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)

    def valid(self):
        if not self.expire_at:
            return False
        return self.expire_at > timezone.now()

    @jsonGetter(name="username")
    def username(self):
        return self.user.username if self.user else None
    
    @jsonGetter(name="ua_cut")
    def ua_cut(self):
        return self.user_agent[:20] if self.user_agent else None

    @staticmethod
    def get_device_info_from_request(request: HttpRequest) -> dict[str, str]:
        if not request:
            return {}
        devices = [
            "android",
            "iphone",
            "ipad",
            "windows phone",
            "mac",
            "windows",
            "linux",
            "maxbook",
        ]
        browsers = ["chrome", "safari", "firefox", "edge"]
        user_agent = request.META.get("HTTP_USER_AGENT") or ""
        browser = next(
            (browser for browser in browsers if browser in user_agent.lower()),
            "unknown",
        )
        browser_version = re.match(
            r".*?{}\/([\d.]+)".format(browser), user_agent.lower()
        )
        browser_version = browser_version.group(1) if browser_version else "unknown"

        platform = request.META.get("HTTP_SEC_CH_UA_PLATFORM")
        if not platform:
            platform = re.match(r".*?\((.*?)\)", user_agent.lower())
            platform = platform.group(1) if platform else "unknown"
        return {
            "user_agent": user_agent,
            "ip": request.META.get("REMOTE_ADDR")
            or request.META.get("HTTP_X_FORWARDED_FOR")
            or request.META.get("HTTP_X_REAL_IP"),
            "device": next(
                (device for device in devices if device in user_agent.lower()),
                "unknown",
            ),
            "platform": platform,
            "browser": browser,
            "version": browser_version,
            "language": request.META.get("HTTP_ACCEPT_LANGUAGE"),
            "sec_ua": request.META.get("HTTP_SEC_CH_UA"),
        }  # type: ignore

    @staticmethod
    def create_token(user: User, request: HttpRequest):
        expire_at = timezone.now() + timedelta(days=1)
        while True:
            token_str = uuid.uuid4()
            if not UserToken.objects.filter(token=token_str.hex).exists():
                break
        token = UserToken.objects.create(
            user=user,
            token=token_str.hex,
            expire_at=expire_at,
            **{
                k: v
                for k, v in UserToken.get_device_info_from_request(request).items()
                if v
            },
        )
        return token

    @staticmethod
    def find_user_by_token(token):
        token = UserToken.objects.filter(token=token).first()
        if not token:
            return None
        
        return token.user

    @staticmethod
    def get_fresh_token_by_user(user: User, request: HttpRequest):
        device_info = UserToken.get_device_info_from_request(request)
        token = UserToken.objects.filter(user=user).order_by("-created_at").first()

        #  不同设备，重新生成token
        if not token or token.user_agent != device_info["user_agent"] or token.ip != device_info["ip"] or token.device != device_info["device"] or token.platform != device_info["platform"]:
            return UserToken.create_token(user, request=request)
        
        #  token已过期，重新生成
        if not token.valid():
            return UserToken.create_token(user, request=request)
        
        #  token有效，不需要重新生成，并延长有效期，更新设备信息
        token.expire_at = timezone.now() + timedelta(days=1)
        for k, v in UserToken.get_device_info_from_request(request).items():
            setattr(token, k, v)
        token.save()
        return token
    

    @staticmethod
    def set_invalid_by_token(token):
        token = UserToken.objects.filter(token=token).first()
        if not token:
            return False
        token.expire_at = timezone.now() - timedelta(minutes=5)
        token.save()
        return True
