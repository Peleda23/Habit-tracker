from django.contrib import admin

from .models import Habit, HabitEntry


class HabitAdmin(admin.ModelAdmin):
    model = Habit
    list_display = ["user", "name", "description"]


class HabitEntryAdmin(admin.ModelAdmin):
    def get_user(self, obj):
        return obj.habit.user

    get_user.short_description = "User"
    model = HabitEntry
    list_display = ["get_user", "habit", "date", "value"]

    def save_model(self, request, obj, form, change):
        # Automatically set the user based on the selected habit
        obj.user = obj.habit.user
        super().save_model(request, obj, form, change)


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitEntry, HabitEntryAdmin)
