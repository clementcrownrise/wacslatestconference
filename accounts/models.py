from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from faculty.models import Faculty


class MyAccountManager(BaseUserManager):

    def create_user(
        self,
        email,
        username,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address.")

        if not username:
            raise ValueError("Users must have a username.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superadmin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )


class Account(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        ("candidate", "Candidate"),
        ("reviewer", "Reviewer"),
        ("admin", "Admin"),
        ("staff", "Staff"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    username = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField(
        max_length=100,
        unique=True
    )

    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="candidate"
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_admin

    def has_module_perms(self, app_label):
        return True
