from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.CharField(max_length=200, blank=True, verbose_name='описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Measurement(models.Model):
    temperature = models.DecimalField(verbose_name='температура', max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='измерено')
    changed_in = models.DateTimeField(auto_now=True, verbose_name='изменено')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.created_at}, {self.sensor}: {self.temperature}'
