from django.contrib import admin

from .models import Habit, HabitEntry


class HabitAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "description"]


class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ["habit", "date", "value"]


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitEntry, HabitEntryAdmin)
