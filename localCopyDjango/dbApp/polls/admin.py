from django.contrib import admin

# Register your models here.
from .models import User, Restaurant,Menu, Hours
admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Hours)
