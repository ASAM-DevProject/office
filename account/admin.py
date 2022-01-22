from django.contrib import admin
from account import models
from django.contrib.auth.admin import UserAdmin

UserAdmin.fieldsets += ('Role', {'fields':('user_type', 'is_sick', 'is_doctor', 'is_secretary')}),

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type')

UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'is_email_verify')

class SpecialtiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    ordering = ('title',)
    search_fields = ('title', 'slug')

class ProfileSickAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_code', 'is_sick')
    ordering = ('id',)
    search_fields = ('first_name', 'last_name', 'national_code')

class ProfileDoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'expertise', 'is_doctor')
    ordering = ('id',)
    search_fields = ('first_name', 'last_name', 'expertise')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Specialties, SpecialtiesAdmin)
admin.site.register(models.ProfileSick, ProfileSickAdmin)
admin.site.register(models.ProfileDoctor, ProfileDoctorAdmin)