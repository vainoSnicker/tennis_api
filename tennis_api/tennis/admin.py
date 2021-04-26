from django.contrib import admin
from .models import Player, Tourney, Match


admin.site.register(Player)
admin.site.register(Tourney)
admin.site.register(Match)
