from django.contrib import admin
from blog.models import Article, Category, Comment, ContactUs, Like


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "title", "auther", "show_image")
    list_editable = ("title",)
    list_filter = ("auther",)
    search_fields = ("title", "body")
    exclude = ("slug",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("body", "article", "author")


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("title", "text")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ("slug",)


admin.site.register(Like)
