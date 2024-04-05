from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Quote)
admin.site.register(Message)
admin.site.register(UserComment)
admin.site.register(Post)
admin.site.register(Product)