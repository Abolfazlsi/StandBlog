from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Category, self).save()

    def get_absolute_url(self):
        return reverse("blog:category_detail", args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Article(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    category = models.ManyToManyField("blog.Category", related_name="articles", verbose_name="دسته بندی")
    title = models.CharField(max_length=50, verbose_name="عنوان")
    body = models.TextField(verbose_name="بدنه")
    image = models.ImageField(upload_to="images/articles", blank=True, null=True, verbose_name="عکس")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, unique=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now(), verbose_name="تاریخ")

    class Meta:
        ordering = ("-created",)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def show_image(self):
        if self.image:
            return format_html(f"<img src='{self.image.url}' width='70px' height='50px'>")
        return format_html("<h3 style='color: red;'>تصویر ندارد</h3>")

    show_image.short_description = "عکس مقالات"

    def get_absolute_url(self):
        return reverse("blog:article-detail", args=[self.slug])

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="نویسنده")
    article = models.ForeignKey("blog.Article", on_delete=models.CASCADE, related_name="comments", verbose_name="مقاله")
    body = models.TextField(verbose_name="بدنه")
    created = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies",
                               verbose_name="ریپلای")

    class Meta:
        ordering = ("-created",)
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.author} - {self.body[:30]}"


class ContactUs(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name="عنوان")
    text = models.TextField(verbose_name="پیام")
    email = models.EmailField(verbose_name="ایمیل")
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.text[:30]}"

    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "تماس با ما"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="کابر")
    article = models.ForeignKey("blog.Article", on_delete=models.CASCADE, related_name="likes", verbose_name="مقاله")

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
