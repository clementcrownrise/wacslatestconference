from django.contrib import admin
from .models import Conference



class ConferenceAdmin(admin.ModelAdmin):
        list_display = ('name',)

    

admin.site.register(Conference, ConferenceAdmin)
