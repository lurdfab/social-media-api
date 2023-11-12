from django.db import models

class Comment(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment_image = models.ImageField(upload_to='comment_images/', blank=True, null=True)

    def __str__(self):
        return self.comment