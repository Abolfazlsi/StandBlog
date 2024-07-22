from django.shortcuts import render, redirect
from blog.models import Article
from django.urls import reverse


def home(request):
    articles = Article.objects.all()
    updated_articles = Article.objects.all().order_by("-updated")[:3]

    context = {
        "articles": articles,
        "updated_articles": updated_articles,
    }
    return render(request, "home/index.html", context)


def sidebar(request):
    context = {
        "name": "Abolfazl"
    }
    return render(request, "includes/sidebar.html", context)
