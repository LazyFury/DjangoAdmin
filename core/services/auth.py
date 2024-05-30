import re
from common.exception import ApiError, ApiNotAuthorizedError, ApiNotFoundError
from core.models import User
from django.contrib.auth.hashers import make_password


class AuthService:
    use_email: bool = False
    use_phone: bool = False
    use_username: bool = False

    def __init__(
        self,
        use_email: bool = True,
        use_phone: bool = False,
        use_username: bool = False,
    ):
        self.use_email = use_email
        self.use_phone = use_phone
        self.use_username = use_username

    def validate_email(self, email: str) -> tuple[bool, str]:
        if User.objects.filter(email=email).exists():
            return False, "Email already exists"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email"
        if len(email) > 255:
            return False, "Email too long"
        return True, ""

    def validate_phone(self, phone: str) -> tuple[bool, str]:
        if User.objects.filter(phone=phone).exists():
            return False, "Phone already exists"
        if not re.match(r"^\+?1?\d{9,15}$", phone):
            return False, "Invalid phone"
        return True, ""

    def validate_username(self, username: str) -> tuple[bool, str]:
        if User.objects.filter(username=username).exists():
            return False, "Username already exists"
        if len(username) > 150:
            return False, "Username too long"
        return True, ""

    def authenticate(
        self, email: str = "", phone: str = "", username: str = "", password: str = ""
    ) -> User:
        assert email or phone or username,"必须传入用户唯一标识或emial或phone"
        
        query = User.objects.filter()
        if email:
            query = query.filter(email=email)
        if phone:
            query = query.filter(phone=phone)
        if username:
            query = query.filter(username=username)

        user = query.first()
        print(query.query)
        assert user, "User Not Found."
        if user.check_password(password):
            return user
        raise ApiNotAuthorizedError("Password Not Right.")

    def register(
        self,
        email: str = "",
        phone: str = "",
        username: str = "",
        password: str = "",
        **kwargs,
    ):
        assert email or phone or username,"必须传入用户唯一标识或emial或phone"
        
        if email:
            valid, msg = self.validate_email(email)
            if not valid:
                raise ApiError(msg)

        if phone:
            valid, msg = self.validate_email(phone)
            if not valid:
                raise ApiError(msg)

        if username:
            valid, msg = self.validate_email(username)
            if not valid:
                raise ApiError(msg)

        password = make_password(password)
        user = User.objects.create(
            **{"email": email, "phone": phone, "username": username, **kwargs}
        )
        return user
