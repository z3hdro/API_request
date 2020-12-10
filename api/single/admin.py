from django.contrib import admin
from single.models import Link


# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'time', 'status', 'description', 'timeout')


admin.site.register(Link, LinkAdmin)
