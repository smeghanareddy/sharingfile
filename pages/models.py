from django.contrib.auth.models import User
from django.db import models


class Documents(models.Model):
    """
    saving uploaded files in database
    """
    title = models.CharField(max_length=100)
    image = models.ImageField()
    pdf = models.FileField()
    description = models.CharField(max_length=100)
    c_on = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()  # deleting pdf files
        self.image.delete()  # deleting images files
        super().delete(*args, **kwargs)


class Profile(models.Model):
    """
    for extending User model with user type
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #  choices=(("admin", "Admin"),)
    user_type = models.CharField(max_length=5,)

    def __str__(self):
        """
        Returning profile details
        :return: fields of activity transaction
        """
        return f"{self.user}, {self.user_type}"
