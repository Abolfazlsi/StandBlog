from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    fathers_name = models.CharField(max_length=50, verbose_name="نام پدر")
    melicode = models.CharField(max_length=10, verbose_name="کد ملی")
    image = models.ImageField(upload_to="images/profiles", blank=True, null=True, verbose_name="عکس کاربر")

    def __str__(self):
        return self.user.username

    def show_image(self):
        return format_html(f"<img src='{self.image.url}' width='50px' height='50px'>")

    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب های کاربری"
