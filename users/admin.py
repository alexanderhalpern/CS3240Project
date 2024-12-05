from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'is_pma_admin', 'profile_picture'] 
    list_filter = ['is_pma_admin'] 
    search_fields = ['user__username', 'user__email']   
admin.site.register(Profile, ProfileAdmin)