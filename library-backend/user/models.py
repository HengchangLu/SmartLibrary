from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20)
    account = models.CharField(max_length=10, primary_key=True)
    gender = models.CharField(max_length=5)
    dept_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['student_id']

    def __str__(self):
        user_info = "  "
        seq = (self.account, self.student_id, self.name, self.gender, self.dept_name)
        return user_info.join(seq)


class FeedbackInfo(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20)
    account = models.CharField(max_length=10, primary_key=True)
    gender = models.CharField(max_length=5)
    dept_name = models.CharField(max_length=30)
    feedback_msg = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
