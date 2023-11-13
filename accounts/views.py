from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Follow, CustomUser
from goods.models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from django.db.models import Prefetch
from .tasks import send_product_list
from django.http import HttpResponse


class ProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'account/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.kwargs.get('username'))

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('products', queryset=Product.objects.all(), to_attr='product_list')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context['following'] = Follow.objects.filter(
            user=self.request.user,
            author=user
        ).exists()
        context['followers_count'] = Follow.objects.filter(author=user).count()
        context['products'] = Product.objects.filter(author=user, available=True)
        context['products_count'] = context['products'].count()
        return context


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


class ProfileUpdate(UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'account/profile_update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.object.username})


def send_email_user(request):
    if request.user.is_authenticated:
        send_product_list.delay(request.user.id)
        return redirect('accounts:profile', username=request.user.username)
    else:
        return HttpResponse('User is not authenticated')
