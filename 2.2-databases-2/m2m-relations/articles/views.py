from django.shortcuts import render

from articles.models import Article, Tag, ArticleScope


def articles_list(request):
    template = 'articles/news.html'
    context = {}

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = '-published_at'
    # articles = Article.objects.all()
    # 'object_list': Article.objects.prefetch_related('tags').all().order_by(ordering)
    context = {
        'object_list': Article.objects.prefetch_related('tags').all().order_by(ordering),
        # 'article.scopes.all': ArticleScope.objects.filter(id=1).order_by('is_main')
    }
    return render(request, template, context)
