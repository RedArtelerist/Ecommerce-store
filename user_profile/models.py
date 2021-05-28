from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,
                              upload_to='profiles',
                              default='profiles/placeholder.png')
    middle_name = models.CharField(max_length=30, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, default=1)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=30, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/profiles/placeholder.jpg'
        return url


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

