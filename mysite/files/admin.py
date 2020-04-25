from django.contrib import admin
from .models import ImageFile, VideoFile, DownloadableFile
# Register your models here.


admin.site.register(VideoFile)
admin.site.register(ImageFile)
admin.site.register(DownloadableFile)
