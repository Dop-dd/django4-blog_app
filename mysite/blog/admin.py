from django.contrib import admin
from .models import Post

#admin.site.register(Post)
@admin.register(Post)
# model is registered in the site using a custom class that inherits from ModelAdmin
class PostAdmin(admin.ModelAdmin):
    # set the fields of your model that you want to display on the administration object list page
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
