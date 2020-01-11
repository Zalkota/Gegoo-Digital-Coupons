from django.contrib import admin
from .models import Contact

from support import models as support_models

class QuestionAdmin(admin.ModelAdmin):
    list_display            = ('title', 'topic', 'slug', 'status', 'created_at', 'updated_at')
    list_filter             = ('status', 'created_at', 'updated_at')
    search_fields           = ('title', 'status')
    prepopulated_fields     = {'slug':('title',)}
    list_editable           = ('status', 'topic')
    date_hierarchy          = ('created_at')

class TopicAdmin(admin.ModelAdmin):
    list_display            = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields     = {'slug':('title',)}
    list_filter             = ('created_at', 'updated_at')
    search_fields           = ('title',)
    date_hierarchy          = ('created_at')

admin.site.register(support_models.Question, QuestionAdmin)
admin.site.register(support_models.Topic, TopicAdmin)
admin.site.register(Contact)
