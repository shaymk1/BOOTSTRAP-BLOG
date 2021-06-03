from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from marketing.models import Signup
from .forms import CommentForm, PostForm

# Create your views here.


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None
# def get_author(user):
#     queryset = Author.objects.filter(user=user)
#     if queryset.exists():
#         return queryset[0]
#     return None
def search_results(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)

        ).distinct()

        context = {

            "queryset": queryset
        }

        return render(request, "myblog/search_results.html", context)


def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))
    return queryset


def home(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, "myblog/home.html", context)


def blog(request):
    category_count = get_category_count()
    # print(category_count)
    most_recent = Post.objects.order_by("-timestamp")[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)

    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)

    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        # "post_list": post_list,
        "category_count": category_count,
        "most_recent": most_recent,
        "queryset": paginated_queryset,
        "page_request_var": page_request_var
    }
    return render(request, "myblog/blog.html", context)


def post(request, pk):
    post = get_object_or_404(Post,  pk=pk)
    category_count = get_category_count()
    most_recent = Post.objects.order_by("-timestamp")[:4]
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={'pk': post.pk}))
    context = {"post": post,
               "category_count": category_count,
               "most_recent": most_recent,
               "form": form
               }
    return render(request, "myblog/post.html", context)


def post_create(request):
    title = "Create"
    form=PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method=='POST':
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect(reverse('post-detail', kwargs={'pk': post.pk}))

    context = {

        "form":form,
        "title": title
        # "author": author
    }

    
    return render(request, "myblog/post_create.html", context)


def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': form.instance.pk
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "myblog/post_create.html", context)


def post_delete(request, pk):
    post = get_object_or_404(Post,  pk=pk)
    post.delete()
    return redirect(reverse("blog"))
    
# def post_update(request, pk):
#     title = "Update"
#     post = get_object_or_404(Post,  pk=pk)
#     form = PostForm(request.POST or None, request.FILES or None, instance=post)
#     author = get_author(request.user)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.instance.author = author
#             form.save()
#             return redirect(reverse('post-detail', kwargs={'pk': post.pk}))

#     context = {

#         "form": form,
#         "title": title
#         # "author": author
#     }
#     return render(request, "myblog/post_create.html")


# def post_delete(request, pk):
#     title = "Delete"
#     post = get_object_or_404(Post,  pk=pk)
#     form = PostForm(request.POST or None, request.FILES or None, instance=post)
#     author = get_author(request.user)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.instance.author = author
#             form.save()
#             return redirect(reverse('post-detail', kwargs={'pk': post.pk}))

#     context = {

#         "form": form,
#         "title": title
#         # "author": author
#     }
#     return render(request, "myblog/post_delete.html")

    #    most_recent = Post.objects.get(slug=slug)
    #    context = {
    #         "post": most_recent
    #     }
    #    return HttpResponseRedirect(reverse("post", args=[slug]))


# def post_detail(request, id):
#     return render(request, "myblog/post_detail.html")
