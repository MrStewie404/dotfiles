from django.db.models import Sum
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User as UserModel
import time

news = 'NE'
article = 'AR'
CONTENT_TYPE = [
    (news, 'Новость'),
    (article, 'Статья')
]

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField()
    date_registration = models.DateField()

    def create_user(self, first_name, last_name, username):
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            date_registration=time.strftime('%Y-%m-%d')
        )
        user.save()


class Author(models.Model):
    user = models.OneToOneField("User", on_delete = models.CASCADE)
    rating = models.FloatField()
    def update_rating(self):
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))
        temp_sum_p = int(post_sum.get('postRating'))
        comment_sum = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = int(comment_sum.get('commentRating'))

        self.rating = temp_sum_p * 3 + temp_sum_c
        self.save()
    
    def create_author(self, id):
        author = Author(rating = 0, user_id = id)
        author.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.TextField(unique = True, help_text=_('category name'))
    subscribers = models.ManyToManyField(UserModel, related_name='categories')

    def create_category(self, name):
        category = Category(name = name)
        category.save()

    def __str__(self):
        return self.name
    
class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete = models.CASCADE)
    category = models.ForeignKey("Category", on_delete = models.CASCADE)

class Post(models.Model):
    content_type = models.CharField(max_length = 2,
                                  choices = CONTENT_TYPE,
                                  default = article)
    author = models.ForeignKey("Author", on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField("Category", through='PostCategory')
    title = models.TextField()
    text = models.TextField()
    rating = models.FloatField(default=0)

    def set_now_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def create_post(self, content_type: str = 'Новость | Статья', 
                    author: int = 2, 
                    category: str = 'Игры | Музыка | Интернет | Искусство', 
                    title: str = "...", 
                    text: str = "..."):
        post = Post(content_type = content_type,
                    author = author,
                    datetime = Post().set_now_time(),
                    category = category,
                    title = title,
                    text = text,
                    rating = 0)
        post.save()

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()

    def preview(self):
        # post = Post.objects.filter(id = id).first()
        return f"{self.text[:124]}{'...' if len(self.text) > 124 else ''}"
    
    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
                

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete = models.CASCADE)
    user = models.ForeignKey("User", on_delete = models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def set_now_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )