from django.contrib import admin
from .models import Livre, Dvd, Cd

# Register your models here.
admin.site.register(Livre)
admin.site.register(Dvd)
admin.site.register(Cd)

