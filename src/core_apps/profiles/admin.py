from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "email", "gender", "phone_number", "country", "city"]
    list_display_links = ["pkid", "id", "user"]
    list_filter = ["id", "pkid"]
    readonly_fields = ["email"]  # Make email field read-only

    def email(self, obj):
        return obj.user.email  # Assuming email is a field on the related user model

    email.short_description = 'Email'

    # Only include editable fields in the fields attribute
    fields = (
        "user", 
        "email",  # Placing email immediately below user
        "gender", 
        "phone_number", 
        "country", 
        "city"
    )


admin.site.register(Profile, ProfileAdmin)
