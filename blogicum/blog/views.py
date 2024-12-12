from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404

from .models import Post, Category

POSTS_LIMIT = 5


def index(request):
    posts = (
        Post.objects
        .select_related('category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )[:POSTS_LIMIT]
    )
    return render(
        request,
        'blog/index.html',
        context={
            'post_list': posts,
            'title': 'Лента записей',
        }
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
        )

    return render(
        request,
        'blog/detail.html',
        context={
            'post': post,
            'title': 'Пост'
        },
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("В данной категории нет постов")

    posts_in_category = (
        Post.objects
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now()
        )
    )

    return render(
        request,
        'blog/category.html',
        context={
            'category': category,
            'post_list': posts_in_category,
        }
    )
