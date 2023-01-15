from django.contrib import admin
from .models.ballkid import *
from .models.schedule import *

# Register your models here.

admin.site.register(Ballkid)
admin.site.register(Schedule)
admin.site.register(CheckinHistory)
admin.site.register(TeamHistory)
admin.site.register(CheckinAnalytics)
admin.site.register(CourtAnalytics)
admin.site.register(CaptainAnalytics)
admin.site.register(CaptainHistory)
