from django.contrib import admin
from simple_sis.models import (
    User,
    UserAccountType,
    School,
    Activity,
    Location,
    Venue,
    LookupCode,
    LookupCodeType,
)


class UserAdmin(admin.ModelAdmin):
    pass


class UserAccountTypeAdmin(admin.ModelAdmin):
    pass


class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'location',
    )


class ActivityAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class VenueAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'location',
    )


class LookupCodeAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'type',
    )


class LookupCodeTypeAdmin(admin.ModelAdmin):
    pass


# Set header
admin.site.site_header = 'SimpleSIS Admin'

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(UserAccountType, UserAccountTypeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LookupCode, LookupCodeAdmin)
admin.site.register(LookupCodeType, LookupCodeTypeAdmin)
