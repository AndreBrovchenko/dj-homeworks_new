from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, ArticleScope


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data:
                if form.cleaned_data['is_main']:
                    is_main_count += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if is_main_count < 1:
            raise ValidationError('Укажите основной раздел')
        elif is_main_count > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleScopeInline(admin.TabularInline):
    list_display = ['name']
    model = ArticleScope
    formset = ArticleScopeInlineFormset
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ArticleScopeInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
    inlines = [ArticleScopeInline]
