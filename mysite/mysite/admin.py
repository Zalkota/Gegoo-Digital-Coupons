from django.contrib import admin

# Define a new FlatPageAdmin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget





# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage)
