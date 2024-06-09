from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([Test, Subject, Category, Result])
