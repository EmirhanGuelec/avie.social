from django.db import models

class Post(models.Model):
    author = models.CharField(max_length=150)  
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post von {self.author} am {self.created_at}"  

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=150)  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kommentar von {self.author}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    username = models.CharField(max_length=150)  

    class Meta:
        unique_together = ('post', 'username')  # Jeder Nutzer darf nur einmal liken

    def __str__(self):
        return f"{self.username} liked Post {self.post.id}"
