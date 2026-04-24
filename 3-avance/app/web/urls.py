from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="articles"), name="home"),
    path("home", RedirectView.as_view(url="articles"), name="home"),

    path("articles", views.ArticleListView.as_view(), name="article_list"),
    path("publications", views.PublicationsView.as_view(), name="publications"),
    path("favourites", views.FavouritesView.as_view(), name="favourites"),
    path("publication", views.PublicationView.as_view(), name="publication"),
    path("detail/<int:pk>", views.ArticleDetailView.as_view(), name="detail"),
    path("favourite/<int:pk>", views.AddToFavouritesView.as_view(), name="add_to_favourites"),

    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path("register", views.UserRegisterView.as_view(), name="register"),

]