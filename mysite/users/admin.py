from django import forms
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users import models as users_models
from portal import models as portal_models

# class ProfileInline(admin.StackedInline):
#     model = users_models.Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'

# class StoreInline(admin.TabularInline):
#     model = portal_models.Store.merchant.MerchantProfile.through
#     # autocomplete_fields = ['city']


class StoreInlineAdmin(admin.TabularInline):
    model = portal_models.Store

class UserAdmin(admin.ModelAdmin):
    list_display            = ('username', 'first_name', 'last_name', 'is_merchant', 'created_at', 'updated_at')
    list_filter             = ('created_at', 'updated_at')
    search_fields           = ('username', 'first_name', 'last_name')
    # prepopulated_fields     = {'slug':('username',)}
    # list_editable           = ('is_merchant')
    date_hierarchy          = ('created_at')

    inlines = [
        StoreInlineAdmin,
    ]

admin.site.register(users_models.User, UserAdmin)
admin.site.register(users_models.Profile)
admin.site.register(users_models.MerchantProfile)
admin.site.register(users_models.Follow)

# @admin.register(userStripe)
# class userStripeAdmin(admin.ModelAdmin):
#     model = userStripe

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile


# class MyUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = User


# class MyUserCreationForm(UserCreationForm):

#     error_message = UserCreationForm.error_messages.update({
#         'duplicate_username': 'This username has already been taken.'
#     })

#     class Meta(UserCreationForm.Meta):
#         model = User

#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(self.error_messages['duplicate_username'])


# @admin.register(User)
# class MyUserAdmin(AuthUserAdmin):
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
#     fieldsets = AuthUserAdmin.fieldsets
#     list_display = ('username', 'name', 'is_superuser')
#     search_fields = ['name']
