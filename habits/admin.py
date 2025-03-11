from django.contrib import admin

from .models import Habit


class HabitAdmin(admin.ModelAdmin):
    list_display = ["user", "description"]


admin.site.register(Habit, HabitAdmin)
