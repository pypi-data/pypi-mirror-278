from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model

from drf_api_auth.models import ApiAuth


User = get_user_model()


class ApiAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'created')
    fields = ('user', 'api_key')
    readonly_fields = ("created", )
    search_fields = ('user__username',)
    search_help_text = 'Username'
    ordering = ('-created',)

    @admin.display(description='User')
    def get_user(self, obj):
        user = obj.user
        url = reverse(
            'admin:%s_%s_change' % (User._meta.app_label, User._meta.model_name), args=(quote(user.pk),),
            current_app=self.admin_site.name
        )
        return format_html(f'<a href="{url}">{user}</a>')


admin.site.register(ApiAuth, ApiAuthAdmin)
