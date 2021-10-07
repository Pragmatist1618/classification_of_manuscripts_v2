from django.contrib.auth.models import User
from django.db import models


# модель рукописи
class Manuscript(models.Model):
    # место хранения
    storage = models.CharField(max_length=100, null=True, blank=True)
    # дата создания
    creation_date = models.CharField(max_length=25, default='Неизвестно')
    creation_date_bgn = models.CharField(max_length=25, null=True, blank=True)
    creation_date_end = models.CharField(max_length=25, null=True, blank=True)
    # название (шифр рукописи)
    # (unique=True) - Наименование должно быть уникально
    cipher = models.CharField(max_length=30, unique=True)


    TYPE_CHOICES = [
        ("Tetr", 'Четвероевангелие'),
        ('Lect', 'Лекционарий'),
        ('unknown', 'неизвестно'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    LEC_TYPE_CHOICES = [
        ("le", 'полный'),
        ('Lesk', 'краткий'),
        ('Lesel', 'праздничный'),
        ('unknown', 'неизвестно'),
    ]
    lec_type = models.CharField(max_length=15, choices=LEC_TYPE_CHOICES, null=True, blank=True)

    man_description = models.TextField(max_length=500, null=True, blank=True)
    # description = models.JSONField(null=True, blank=True)
    bibliography = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.cipher


# class Part_of_manuscript(models.Model):
#     manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='part')
#
#
# class Page(models.Model):
#     part = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='images')


# Создаем отдельную модель для изображений, чтобы иметь возможность к одной записи
# добавлять сразу несколько изображений
class Image(models.Model):
    # путь к изображению
    image = models.ImageField()
    # к какой рукописи относится
    # Каскадное удаление. Django эмулирует поведение SQL правила ON DELETE CASCADE
    # и так же удаляет объекты, связанные через ForeignKey
    # (related_name='images') - для получения полей таблицы через сереалайзер рукописи
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='images')
    creation_date = models.CharField(max_length=25, default='Неизвестно', null=True, blank=True)
    creation_date_bgn = models.CharField(max_length=25, null=True, blank=True)
    creation_date_end = models.CharField(max_length=25, null=True, blank=True)
    folio_number = models.CharField(max_length=5)
    part_of_folio = models.CharField(max_length=50, null=True, blank=True)




    LEC_PART_CHOICES = [
        ("sin", 'Синаксарь'),
        ('men', 'Менологий'),
        ('unknown', "Неизвестно"),
    ]
    lec_part_type = models.CharField(max_length=15, choices=LEC_PART_CHOICES, null=True, blank=True)
    # если синаксарь, то дальше - Евангелие
    # если менологий, то дельше - месяц, а потом Евангелие
    LEC_MONTH_CHOICES = [
        ("St", 'сентябрь'),
        ('Ok', 'октябрь'),
        ('Nw', 'ноябрь'),
        ('Dec', 'декабрь'),
        ("Ja", 'январь'),
        ('Feb', 'февраль'),
        ('Mar', 'март'),
        ('Apr', 'апрель'),
        ("May", 'май'),
        ('Jun', 'июнь'),
        ('Jul', 'июль'),
        ('Aug', 'август'),
        ('unknown', 'неизвестно'),
    ]
    lec_month_type = models.CharField(max_length=15, choices=LEC_MONTH_CHOICES, null=True, blank=True)

    # Указатель на Евангелия
    GOSPEL_CHOICES = [
        ('Matthew', 'Матфея'),
        ('Luke', 'Луки'),
        ('Mark', 'Марка'),
        ('John', 'Иоанна'),
        ('unknown', 'неизвестно'),
    ]
    # (choices=GOSPEL_CHOICES) - варианты поля
    # какое Евангелие
    gospel = models.CharField(max_length=10, choices=GOSPEL_CHOICES)
    # глава
    chapter = models.CharField(max_length=2, null=True, blank=True)
    # стих (абзац)
    verse = models.CharField(max_length=2, null=True, blank=True)
    verse_quote = models.CharField(max_length=5, null=True, blank=True)
    image_name = models.CharField(max_length=50, null=True, blank=True)
    img_description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.id)

