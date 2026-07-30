from django.urls import path
from quickstart import views

urlpatterns = [
    path("say/", views.say_view, name="say"),
]
