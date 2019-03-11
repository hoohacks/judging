from django.contrib import admin

from .models import *

admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Criteria)
admin.site.register(CriteriaLabel)
admin.site.register(Demo)
admin.site.register(DemoScore)
