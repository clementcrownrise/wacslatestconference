from django.contrib import admin
from .models import Conferencename
from confregdetails.models import Confregdetail

# Register your models here.

class ConfregdetailInline(admin.TabularInline):
    model = Confregdetail
    extra = 0

class ConferencenameAdmin(admin.ModelAdmin):
        list_display = ('name',)
        inlines = [ConfregdetailInline]


admin.site.register(Conferencename, ConferencenameAdmin)
