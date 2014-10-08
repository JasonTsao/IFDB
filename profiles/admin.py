from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from models import *

admin.site.register(Profile)
admin.site.register(CollaborationLink)