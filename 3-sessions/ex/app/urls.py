from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("disconnect", views.disconnect, name="disconnect"),
    path("vote/<int:tip_id>", views.vote, name="vote"),
    path("destroy/<int:tip_id>", views.destroy, name="destroy"),
]