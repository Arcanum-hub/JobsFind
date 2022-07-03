
from email.policy import default
from sqlite3 import Timestamp
from tabnanny import verbose
from django.db import models
from django.forms import JSONField


from scrap.utils import from_cyrillic_to_eng



def default_urls():
    return{'hh': "", 'jooble': "", 'indeed': ""}

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Название населенного пункта', unique=True)
    slug = models.CharField(max_length=50, blank = True, unique=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Специальность', unique=True)
    slug = models.CharField(max_length=50, blank = True, unique=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальность'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('city', on_delete=models.CASCADE, verbose_name='Страна')
    language = models.ForeignKey('language', on_delete=models.CASCADE, verbose_name='Специальность')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)
    

class Url(models.Model):
    city = models.ForeignKey('city', on_delete=models.CASCADE, verbose_name='Страна')
    language = models.ForeignKey('language', on_delete=models.CASCADE, verbose_name='Специальность')
    url_data = models.JSONField(default=default_urls)
    
    class Meta:
        unique_together = ('city', 'language')