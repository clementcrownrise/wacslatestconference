from django.contrib import admin

from .models import Confregdetail
from conferencename.models import Conferencename

from django.http import HttpResponse
from openpyxl import Workbook


@admin.action(description="Export selected registrations to Excel")
def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Registrations"

    # Header row
    ws.append([
        "First Name",
        "Last Name",
        "Email",
        "Conference",
        "Institution",
        "Faculty",
        "Subspecialty",
        "Country",
        "Gender",
        "WACS Fellow",
        "Accompanying Person",
        "Registration Date",
    ])

    # Data rows
    for reg in queryset:
        ws.append([
            reg.user.first_name if reg.user else "",
            reg.user.last_name if reg.user else "",
            reg.user.email if reg.user else "",
            reg.conferencename.name,
            reg.institutionName,
            reg.faculty.faculty_name,
            reg.subspecialty,
            reg.country,
            reg.gender,
            reg.wacsfellow,
            reg.accompany,
            reg.created_at.strftime("%Y-%m-%d"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="conference_registrations.xlsx"'

    wb.save(response)
    return response




class ConferenceregdetilAdmin(admin.ModelAdmin):
        list_display=('user_first_name','user_last_name','user','conferencename',
                       'faculty', 'subspecialty',
                         'institutionName','country',)
        
        list_filter = (
        'conferencename',
        'faculty',
        'country',
                        )
        actions = [export_to_excel]

        
        
        search_fields = (
            'user__first_name',
            'user__last_name',
            'user__email',
            'institutionName',
        )

        @admin.display(description='First Name')
        def user_first_name(self, obj):
            return obj.user.first_name if obj.user else '-'

        @admin.display(description='Last Name')
        def user_last_name(self, obj):
            return obj.user.last_name if obj.user else '-'



admin.site.register(Confregdetail, ConferenceregdetilAdmin)




