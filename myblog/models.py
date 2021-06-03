from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField
from django.shortcuts import redirect

# Create your models here.
User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, db_index=True, null=True)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name="previous", on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name="next", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'pk': self.pk})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return redirect(reverse('post', kwargs={id: self.pk

        # return redirect('post', id=id)
        # return reverse("post", kwargs={
        #     'slug': self.slug
        # })
        # return reverse("post", kwargs={
        #     'id': self.id
        #     })
        # return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        # return reverse("post", kwargs={"slug": self.slug})
