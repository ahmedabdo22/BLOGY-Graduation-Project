from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import NewsletterSubscription


# Create your views here.
@login_required
def subscribe(request, author_id):
    author = get_object_or_404(User,pk=author_id)
    NewsletterSubscription.objects.get_or_create(subscriber=request.user,author=author)
    messages.success(request,"Subscribed successfully.")
    return redirect("accounts:public_profile",username=author.username)

@login_required
def unsubscribe(request, author_id):
    author = get_object_or_404(User,pk=author_id)
    NewsletterSubscription.objects.filter(subscriber=request.user,author=author).delete()
    messages.success(request,"Unsubscribed successfully.")
    return redirect("accounts:public_profile",username=author.username)


@login_required
def my_subscriptions(request):
    subscriptions = (NewsletterSubscription.objects.filter(subscriber=request.user).select_related("author"))
    return render(request,"newsletters/my_subscriptions.html",{"subscriptions": subscriptions})