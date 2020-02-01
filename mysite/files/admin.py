from django.contrib import admin
from .models import FileItem, VideoFile, PromotionalVideo
# Register your models here.


admin.site.register(FileItem)
admin.site.register(VideoFile)
admin.site.register(PromotionalVideo)
