from django.contrib import admin
from .models import Task 

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Колонки, які будуть відображатися у загальному списку в адмінці
    list_display = ('title', 'user', 'is_completed', 'created_at')
    # Фільтри збоку (допомагають швидко відібрати виконані або завдання конкретного юзера)
    list_filter = ('is_completed', 'created_at', 'user')
    # Поля, за якими можна шукати завдання (у верхній частині сторінки з'явиться пошуковий рядок)
    search_fields = ('title', 'description')
    # Дозволяє редагувати статус "виконано" прямо в списку, не заходячи всередину завдання
    list_editable = ('is_completed',)
