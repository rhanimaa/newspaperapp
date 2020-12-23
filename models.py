from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from news.models import Article, Category
from PIL import Image

# Profile class represents all users
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField('date of birth', default=timezone.now)
    liked_articles = models.ManyToManyField(Article, blank=True)
    fav_cats = models.ManyToManyField(Category, blank=True, verbose_name='favourite categories')
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.get_username()

    def save(self,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        newimg = Image.open(self.profile_pic.path)
        img = newimg.convert('RGB')
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)