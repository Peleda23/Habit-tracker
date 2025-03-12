from django.contrib import admin

from .models import Habit, HabitEntry


class HabitAdmin(admin.ModelAdmin):
    model = Habit
    list_display = ["user", "name", "description"]


class HabitEntryAdmin(admin.ModelAdmin):
    model = HabitEntry
    list_display = ["user", "habit", "date", "value"]
    list_filter = ["habit__user"]


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitEntry, HabitEntryAdmin)
