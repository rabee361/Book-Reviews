from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['username','email']
    fieldsets = (
            ('User Information',
                {'fields':('username', 'email','first_name', 'last_name','image','want_to_read','currently_reading','read')}
            ),
            ('Permissions',
                {'fields':('is_staff', 'is_superuser', 'is_active', 'groups','user_permissions')}
            ),
            ('Registration',
                {'fields':('date_joined', 'last_login',)}
        )
    )


admin.site.register(CustomUser , CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Quote)
admin.site.register(Message)
admin.site.register(UserComment)
admin.site.register(Post)
admin.site.register(Product)