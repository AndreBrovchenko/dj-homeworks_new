from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


SORT_MAP = {
    'name': 'name',
    'r_name': '-name',
    'group': 'group',
    'r_group': '-group',
}


def students_list(request):
    template = 'school/students_list.html'
    context = {}
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = request.GET.get('group', 'name')
    if ordering:
        students = Student.objects.prefetch_related('teacher').all().order_by(SORT_MAP[ordering])
    context = {'object_list': students}
    return render(request, template, context)
