from django.contrib import admin

from .models import *

class post_categoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields=('title',)
admin.site.register(post_category,post_categoryAdmin)

class postsAdmin(admin.ModelAdmin):
    list_display = ('title','image','description','post_category','location')
    fields=('title','image','description','post_category','location')
admin.site.register(posts,postsAdmin)

class TurfAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

admin.site.register(Turf)


