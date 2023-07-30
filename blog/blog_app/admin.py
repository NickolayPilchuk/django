from django.contrib import admin
from blog_app.models import UserExtended,Blog,News,Comments
from django.utils.safestring import mark_safe


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name','user','ctime','get_photo')
    def get_photo(self,obj):
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width = "75">')
        else:
            return '-'
    get_photo.short_description = 'Картинка'

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','blog','ctime')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','news', 'user')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'surname','get_photo')
    def get_photo(self,obj):
        if obj.userpic:
            return mark_safe(f'<img src="{obj.userpic.url}" width = "75">')
        else:
            return '-'
    get_photo.short_description = 'Аватар'

admin.site.register(UserExtended,UserAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Comments,CommentAdmin)