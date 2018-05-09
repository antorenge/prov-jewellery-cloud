"""
Users admin views
"""
from django.contrib import admin
from django.template.loader import render_to_string
from .models import User


class UserAdmin(admin.ModelAdmin):
    """Admin view for user profiles"""
    list_display = ('email', 'profile_picture', 'first_name', 'last_name',
                    'phone')

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'phone', 'gender',
                       'picture', 'is_active', 'is_staff')
        }),
        ('Login', {
            'fields': ['email', 'password']
        }),
    )

    def profile_picture(self, obj):
        return render_to_string('picture.html', {
            'picture': obj.picture
        })
    profile_picture.short_description = "Picture"


admin.site.register(User, UserAdmin)
