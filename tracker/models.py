from django.db import models
from django.contrib.auth.models import User # Імпортуємо стандартну модель користувача Django

class Task(models.Model):
    # ForeignKey зв'язує завдання з користувачем. 
    # on_delete=models.CASCADE означає: якщо видалити юзера, видаляться і всі його завдання.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Заголовок завдання (максимум 200 символів)
    title = models.CharField(max_length=200)
    # Детальний опис завдання. null=True дозволяє зберігати порожнє поле в базі.
    description = models.TextField(null=True, blank=True)
    # Статус виконання: True (виконано) або False (не виконано). За замовчуванням — False.
    is_completed = models.BooleanField(default=False)
    # Дата створення. auto_now_add=True автоматично ставить поточний час при створенні запису.
    created_at = models.DateTimeField(auto_now_add=True)

    # Метод __str__ визначає, як об'єкт буде виглядати в адмінці (замість Task object (1) побачимо назву)
    def __str__(self):
        return self.title


# Create your models here.
# python manage.py runserver
# http://127.0.0.1:8000/admin/tracker/task/
# git add .
# git commit -m ""
# git push -u origin main