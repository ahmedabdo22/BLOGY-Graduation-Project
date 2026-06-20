from django.urls import path
from . import views


app_name = "newsletters"

urlpatterns = [

    path(
        "subscribe/<int:author_id>/",
        views.subscribe,
        name="subscribe"
    ),

    path(
        "unsubscribe/<int:author_id>/",
        views.unsubscribe,
        name="unsubscribe"
    ),

    path(
        "my-subscriptions/",
        views.my_subscriptions,
        name="my_subscriptions"
    ),
]