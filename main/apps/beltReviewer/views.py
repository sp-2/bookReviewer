# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
# import bcrypt

def index(request):
  return render(request,'beltReviewer/index.html')

def registerUser(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)

        if 'user' in errors:
            request.session['name'] = errors['user'].name
            request.session['alias'] = errors['user'].alias
            request.session['id'] = errors['user'].id
            request.session['route'] = "registered"
            return redirect('/books')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def loginUser(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)

        if 'user' in errors:
            request.session['name'] = errors['user'].name
            request.session['alias'] = errors['user'].alias
            request.session['id'] = errors['user'].id
            request.session['route'] = "logged in"
            return redirect('/books')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def books(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        print Review.objects.all()
        return render(request,'beltReviewer/success.html',{"all_reviews":Review.objects.all().order_by('-created_at')})

def logout(request):
    request.session.clear()
    return redirect('/')

####################################################

def show_books_add(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        all_books = Book.objects.all()
        unique_authors = {}
        for each_book in all_books:
            unique_authors[each_book.author] = each_book.author
        return render(request,'beltReviewer/add_book_review.html',{'authors': unique_authors})

def process_add_book_add_review(request):

    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        #tbd add check for empty book
        if request.POST['author'] != "":
            author = request.POST['author']
        else:
            author = request.POST['existing_authors']
        print author
        if user:
            book = Book.objects.filter(title = request.POST['title'],author = request.POST['author'])
            if not book:
                newBook = Book.objects.create(title=request.POST['title'],author=author,uploader=user)
                newReview = Review.objects.create(desc=request.POST['review'],rating=request.POST['rating'],reviewer=user,book=newBook)
                book_id = newBook.id
            else:
                newReview = Review.objects.create(desc=request.POST['review'],rating=request.POST['rating'],reviewer=user,book=book[0])
                book_id = book[0].id
        return redirect('/books/'+str(book_id))
    else:
        return redirect('/')

def show_books(request,id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        book2 =  Book.objects.get(id=id)
        return render(request,'beltReviewer/show_book_reviews_add_review.html',{"book":Book.objects.get(id=id)})


def process_add_review(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        if request.method == "POST":
            user = User.objects.get(id=request.session['id'])
            if user:
                book = Book.objects.get(id = request.POST['book_id'])
                if book:
                    newReview = Review.objects.create(desc=request.POST['review'],rating=request.POST['rating'],reviewer=user,book=book)

        return redirect('/books/'+request.POST['book_id'])

def show_user(request,id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request,'beltReviewer/user_show.html',{"user":User.objects.get(id=id)})

def destroy(request,id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        del_review = Review.objects.get(id=id)
        book_id = del_review.book.id
        del_review.delete()
        return redirect('/books/'+str(book_id))
