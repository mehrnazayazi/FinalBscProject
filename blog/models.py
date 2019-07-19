from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    credit = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class BankAccount(models.Model):
    CardNum = models.CharField(max_length=200)
    ExpirationDate = models.DateTimeField
    name = models.CharField(max_length=200, null=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
