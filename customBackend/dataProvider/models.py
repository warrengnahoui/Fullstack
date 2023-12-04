from django.db import models

# Create your models here.


def default_performance():
    return {
        'points': -1,
        'assists': -1,
        'rebounds': -1
    }

class Player(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    team = models.CharField(blank=False, null=False)
    position = models.CharField(blank=False, null=False)
    number = models.CharField(blank=False, null=False)
    picture = models.ImageField(upload_to = 'img', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    match_name = models.CharField(max_length=100, blank=False, null=False)
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, blank=False, null=False)
    stats = models.JSONField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.match_name