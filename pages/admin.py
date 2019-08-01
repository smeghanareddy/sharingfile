from django.contrib import admin
from pages.models import Documents, Profile


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'pdf', 'description', 'c_on')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')


# Register your models here.
admin.site.register(Documents, DocumentAdmin)
admin.site.register(Profile, ProfileAdmin)
