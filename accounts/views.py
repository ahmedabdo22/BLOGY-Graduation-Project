from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from newsletters.models import NewsletterSubscription
from interactions.models import Follow

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            if request.user.is_staff or request.user.is_superuser:
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("core:home")

@login_required
def profile_view(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html")

def public_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    articles = profile_user.articles.filter(
        status="published"
    )

    is_subscribed = False

    if request.user.is_authenticated:
        is_subscribed = NewsletterSubscription.objects.filter(
            subscriber=request.user,
            author=profile_user
        ).exists()

    subscriber_count = NewsletterSubscription.objects.filter(
        author=profile_user
    ).count()

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    return render(
        request,
        "accounts/public_profile.html",
        {
            "profile_user": profile_user,
            "articles": articles,
            "is_subscribed": is_subscribed,
            "subscriber_count": subscriber_count,
            "followers_count": followers_count,
        }
    )
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")

    return render(request, "accounts/edit_profile.html", {"form": form})
