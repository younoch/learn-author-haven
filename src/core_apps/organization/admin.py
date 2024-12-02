from django.contrib import admin
from .models import Organization, OrganizationMember

class OrganizationMemberInline(admin.TabularInline):
    model = OrganizationMember
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'website', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'logo', 'address', 'email', 'phone_number', 'website', 'created_at', 'updated_at')
        }),
    )
    inlines = [OrganizationMemberInline]

class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')
    search_fields = ('user__email', 'organization__name', 'role')
    list_filter = ('role',)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMember, OrganizationMemberAdmin)
