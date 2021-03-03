from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import forms
from . models import CustomUser, Profile


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','is_active' )
    list_filter = ('email',)
    readonly_fields = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', )
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'email',
            }

        # Prevent non-superusers from editing
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'email',
            }


        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled=True

        return form


    # Custom Actions
    actions = [
        'activate_users',
    ]
    

    def activate_users(self, request, queryset):
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f'Activated {cnt} users.')

    activate_users.short_description = 'Activate Users'


    # Overidding user permissions regardless of their permissions.
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


# Register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

# Unregister the Group model from admin.
# since we're not using Django's built-in permissions,
admin.site.unregister(Group)