from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('catalog')


def catalog_view(request):
    template = 'books/books.html'
    # context = {}
    books_list = []
    books = Book.objects.all()
    for book in books:
        book_add = {'name': book.name,
                    'author': book.author,
                    'pub_date': str(book.pub_date)}
        books_list.append(book_add)
    context = {
        'books': books_list
    }
    return render(request, template, context)


def books_view(request, pub_date):
    template = 'books/books.html'
    # context = {}
    books_list = []
    books = Book.objects.filter(pub_date=pub_date).order_by('pub_date')
    previous_books = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date')
    if len(previous_books) > 0:
        book_previous_date = previous_books[0].pub_date
        # print(f'предыдущая дата: {book_previous_date}')
    else:
        book_previous_date = ''
        # print(f'даты ранее {pub_date} нет')
    next_books = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date')
    if len(next_books) > 0:
        book_next_date = next_books[0].pub_date
        # print(f'следующая дата: {book_next_date}')
    else:
        book_next_date = ''
        # print(f'даты позднее {pub_date} нет')
    book_latest_date = Book.objects.latest('pub_date').pub_date
    book_earliest_date = Book.objects.earliest('pub_date').pub_date
    page_tuple = {
        'book_latest_date': str(book_latest_date),
        'book_earliest_date': str(book_earliest_date),
        'book_previous_date': str(book_previous_date),
        'book_next_date': str(book_next_date),
    }
    for book in books:
        book_add = {
            'name': book.name,
            'author': book.author,
            'pub_date': str(book.pub_date)
        }
        books_list.append(book_add)
    context = {
        'books': books_list,
        'page': page_tuple
    }
    return render(request, template, context)
