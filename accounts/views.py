from django.shortcuts import render, redirect, get_object_or_404
from .models import Follow, CustomUser
from goods.models import Product
from django.contrib.auth.decorators import login_required


def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    following = user.following.filter(user=request.user.id).exists()
    followers_count = user.following.count()
    products = Product.objects.filter(author=user.id)
    products_count = products.filter(author=user.id).count()
    context = {
        'profile': user,
        'following': following,
        'followers_count': followers_count,
        'products_count': products_count,
        'products': products,
    }
    return render(request, 'account/profile.html', context=context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(CustomUser, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('accounts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(CustomUser, username=username)
    follower = Follow.objects.filter(user=request.user, author=author)
    if follower.exists():
        if author != request.user:
            follower.delete()
    return redirect('accounts:profile', username=username)
