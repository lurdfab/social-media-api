from django.db import models

class Like(models.Model):
    
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='liked_by_user', default=None, blank=True, null=True)
    disliked_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='disliked_by_user', default=None, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.category
