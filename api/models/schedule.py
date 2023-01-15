from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class Court(models.TextChoices):
    STADIUM = "Stadium"
    HARRIS = "Harris"
    GRANDSTAND = "Grandstand"
    FOUR = "Court 4"
    FIVE = "Court 5"


class Schedule(models.Model):
    day_hour = models.DateTimeField(default=datetime.now)
    team = models.IntegerField(default=0)
    court = models.CharField(max_length=10, choices=Court.choices)
    short_shifted = models.BooleanField(default=False)

    def get_day_str(self):
        return datetime.strftime(self.day_hour, "%Y-%m-%d")

    def get_hour_str(self):
        return datetime.strftime(self.day_hour, "%H:%M")

    def __str__(self):
        return f"Team {self.team} on {self.court} at {self.day_hour}"


class Tournament(models.Model):
    year = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    show_teams = models.BooleanField(default=False)
    show_finals_teams = models.BooleanField(default=False)
    on_rain_delay = models.BooleanField(default=False)
