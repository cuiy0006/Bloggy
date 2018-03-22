from django.db import models

# Create your models here.
class Comment(models.Model):
    commenter = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

class CommentExtension(models.Model):
    comment = models.ForeignKey('comments.Comment', related_name='comment' , on_delete=models.CASCADE)
    under = models.ForeignKey('comments.Comment', related_name='under', on_delete=models.CASCADE)
    replyTo = models.ForeignKey('comments.Comment', related_name='replyTo', on_delete=models.CASCADE)
