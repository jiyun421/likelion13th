from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50) 
    content = models.TextField(null=True, blank=True) # 글자 수 제한이 없는 긴 문자열
    create_at = models.DateTimeField(auto_now_add=True) # 처음 Post 생성시, 현재시간 저장
    member_id = models.ForeignKey(Member, verbose_name="Member", on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.content

class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length = 200, null = True, blank = True)
    post_id = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE, related_name="comments")
    member_id = models.ForeignKey(Member, verbose_name="Member", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content

class Member(models.Model):
    member_id = models.CharField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = EmailField(unique=True)

class UserPost(models.Model):
    member_id = models.ForeignKey(Member, verbose_name="Member", on_delete=models.CASCADE, related_name="userpost")
    post_id = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE, related_name="userpost")