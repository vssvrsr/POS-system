from django.db import models
from appFinal.models import User

# Create your models here.
# class LoggedInUser(models.Model):
#     user = models.OneToOneField(
#         'User',
#         on_delete=models.CASCADE,
#         related_name='logged_in_user',
#     )


class Message(models.Model):
    """
    訊息紀錄
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.TextField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        用來在表示這一筆Message的字串
        """

        return self.message
