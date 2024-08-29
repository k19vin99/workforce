from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Empresa
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'empresa','rut')
    list_filter = ('is_staff', 'is_active', 'groups', 'empresa')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'empresa','rut')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'groups')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'razon_social', 'rut', 'giro', 'cantidad_personal', 'direccion')
    search_fields = ('nombre', 'razon_social', 'rut')
    list_filter = ('giro',)

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
