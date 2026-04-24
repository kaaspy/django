from django.views.generic import ListView, DetailView, CreateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Article, UserFavouriteArticle
from .forms import RegisterUserForm, PublicationForm


class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "publications.html"
    context_object_name = "articles"
    login_url = "login"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

class FavouritesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"
    login_url = "login"

    def get_queryset(self):
        favourites = UserFavouriteArticle.objects.filter(user=self.request.user).values_list("article_id", flat=True)
        return Article.objects.filter(id__in=favourites)
    
class PublicationView(LoginRequiredMixin, CreateView):
    form_class = PublicationForm
    template_name = "publish.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddToFavouritesView(LoginRequiredMixin, RedirectView):
    login_url = "login"

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get("HTTP_REFERER", "")

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get("pk"))

        try:
            favourite = UserFavouriteArticle.objects.get(user=self.request.user, article=article)
            favourite.delete()
            messages.info(request, "Article removed from your favourites")
        except UserFavouriteArticle.DoesNotExist:
            UserFavouriteArticle.objects.create(user=self.request.user, article=article)
            messages.info(request, "Article favourited")

        return super().get(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Login sucessful")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Logged out")
        return super().dispatch(request, *args, **kwargs)

class AnonymousRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

class UserRegisterView(AnonymousRequiredMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "register.html"
    success_url = reverse_lazy("login")
