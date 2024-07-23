from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from blog.models import Article, Category, Comment, ContactUs, Like
from django.core.paginator import Paginator
from blog.forms import ContactUSForm
from django.views.generic.base import View
from django.views.generic import ListView, TemplateView, RedirectView, DetailView, FormView, CreateView, UpdateView, \
    DeleteView, ArchiveIndexView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        "article": article,
        "errors": []
    }

    if request.user.is_authenticated:
        if request.user.likes.filter(article__slug=slug, user_id=request.user.id).exists():
            context["is_liked"] = True
        else:
            context["is_liked"] = False

    if request.method == "POST":
        body = request.POST.get("body")
        parent_id = request.POST.get("parent_id")
        if request.user.is_anonymous:
            context["errors"].append("You are not logged in.")
            return render(request, "blog/article_detail.html", context)

        Comment.objects.create(body=body, article=article, author=request.user, parent_id=parent_id)

    return render(request, "blog/article_detail.html", context)


def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 4)
    page_number = request.GET.get("page")
    objects_list = paginator.get_page(page_number)
    context = {
        "articles": objects_list
    }
    return render(request, "blog/article_list.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all()

    context = {
        "articles": articles
    }
    return render(request, "blog/article_list.html", context)


def search(request):
    q = request.GET.get("q")
    articles = Article.objects.filter(title__icontains=q)
    paginator = Paginator(articles, 1)
    page_number = request.GET.get("page")
    objects_list = paginator.get_page(page_number)

    context = {
        "articles": objects_list,
        "search_term": q
    }
    return render(request, "blog/article_list.html", context)


def contact_us(request):
    if request.method == "POST":
        form = ContactUSForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
    else:
        form = ContactUSForm()

    context = {
        "form": form
    }
    return render(request, "blog/contact_us.html", context)


class HomePageRedirect(RedirectView):
    # url = "/articles/article-list"
    pattern_name = "blog:article-detail"
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        print(self.request.user)
        return super().get_redirect_url(*args, **kwargs)


class ArticleList(TemplateView):
    template_name = "blog/article__list2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Article.objects.all()
        return context


class UserList(ListView):
    queryset = User.objects.all()
    template_name = "blog/user_list.html"


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.likes.filter(article__slug=self.object.slug, user_id=self.request.user.id).exists():
            context["is_liked"] = True
        else:
            context["is_liked"] = False
        return context


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 4


class ContactUsView(FormView):
    template_name = "blog/contact_us.html"
    form_class = ContactUSForm
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        form_data = form.cleaned_data
        ContactUs.objects.create(**form_data)
        return super().form_valid(form)


class MessageView(CreateView):
    model = ContactUs
    fields = ("title", "text")
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = ContactUs
    template_name = "blog/message_list.html"
    context_object_name = "messages"


class MessageUpdateView(UpdateView):
    model = ContactUs
    fields = ("title", "text", "age")
    template_name = "blog/message_update_form.html"
    success_url = reverse_lazy("blog:messages")


class MessageDeleteView(DeleteView):
    model = ContactUs
    success_url = reverse_lazy("blog:messages")


class ArchiveIndexArticleView(ArchiveIndexView):
    model = Article
    date_field = "updated"


def like(request, slug, pk):
    try:
        like = Like.objects.get(article__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({"response": "unliked"})
    except:
        Like.objects.create(article_id=pk, user_id=request.user.id)
        return JsonResponse({"response": "liked"})
