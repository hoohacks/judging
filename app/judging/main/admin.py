from django.contrib import admin

from .models import *

class DemoAdmin(admin.ModelAdmin):
    search_fields = ('team__id', 'judge__id', 'team__table', 'team__name', 'judge__first_name', 'judge__last_name')

admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Criteria)
admin.site.register(CriteriaLabel)
admin.site.register(Demo, DemoAdmin)
admin.site.register(DemoScore)
