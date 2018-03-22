from django.contrib import admin
from blog.models import Post, Category, Tag
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
#admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

# enlarge the textfield of Post-body on admin UI
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':100})}
    }
admin.site.register(Post, PostAdmin)