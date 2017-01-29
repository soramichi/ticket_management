from django.contrib import admin

from .models import Tour, Live, Ticket
# Register your models here.

admin.site.register(Tour)
admin.site.register(Live)
admin.site.register(Ticket)
