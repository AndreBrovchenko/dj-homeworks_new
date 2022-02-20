from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort', '-name')
    context = {}
    phones_list = []
    if sort == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sort == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all().order_by('-name')
    for phone in phones:
        phone_add = {'name': phone.name,
                     'price': phone.price,
                     'image': phone.image,
                     'release_date': phone.release_date,
                     'lte_exists': phone.lte_exists,
                     'slug': phone.slug,
                     }
        phones_list.append(phone_add)
    context = {
        'phones': phones_list,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {}
    phone = Phone.objects.get(slug=slug)
    phone_add = {'name': phone.name,
                 'price': phone.price,
                 'image': phone.image,
                 'release_date': phone.release_date,
                 'lte_exists': phone.lte_exists,
                 'slug': phone.slug,
                 }
    context['phone'] = phone_add
    return render(request, template, context)
