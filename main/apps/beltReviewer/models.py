# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name should be more than 2 characters."
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be more than 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["mail"] = "Email is not valid as it is not in the right format!"
        if not NAME_REGEX.match(postData['name']):
            errors["name_check_2"] = "Name should consist of alphabets only."
        if not NAME_REGEX.match(postData['alias']):
            errors["name_check_3"] = "Alias should consist of alphabets only."
        if len(postData['password']) == 0:
            errors["password"] = "Password cannot be empty!"
        if len(postData['password']) > 8:
            errors["password"] = "Password cannot be more than 8 characters!"
        if postData['password'] != postData['con_password']:
            errors["password_check"] = "Password does not match confirm password!"
        if not len(errors):
            user = User.objects.filter(email = postData['email'])
            if user:
                errors["email_check"] = "This email already exists!"

        if not len(errors):
            pw = postData['password']
            hash_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            newUser = User.objects.create(name=postData['name'],alias=postData['alias'],email=postData['email'],password=hash_pw)
            errors["user"] = newUser

        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors["password_check_2"] = "Password is incorrect!"
            else:
                errors["user"] = user[0]
        else:
            errors["email_check"] = "Login is not valid"

        return errors

# Create your models here.
class User(models.Model):
      name = models.CharField(max_length=255)
      alias = models.CharField(max_length=255)
      email = models.EmailField(max_length=255,unique=True)
      password = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()

      def __repr__(self):
          return 'User(name=%s, alias=%s, email=%s,password=%s created_at=%s,updated_at=%s )'% (self.name, self.alias, self.email, self.password, self.created_at, self.updated_at)


class BookManager(models.Manager):
    def add_book_add_review(self, postData):
        status = {}
        book = Book.objects.filter(title = postData['title'])
        if book:
            status["book_exists"] = True
            status["book"] = book
        else:
            user = User.objects.get(id=request.session.id)
            if user:
                newBook = Book.objects.create(name=postData['title'],alias=postData['author'],uploader=user)
                status["book"] = newBook
        return status

class Book(models.Model):
      title = models.CharField(max_length=255)
      author = models.CharField(max_length=255)
      uploader = models.ForeignKey(User, related_name="books")
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = BookManager()

      def __repr__(self):
          return 'Book(title=%s, author=%s, uploader=%s, created_at=%s,updated_at=%s )'% (self.title, self.author, self.uploader, self.created_at, self.updated_at)

class Review(models.Model):
      desc = models.TextField()
      rating = models.CharField(max_length=255)
      reviewer  = models.ForeignKey(User, related_name="user_reviews")
      book  = models.ForeignKey(Book, related_name="book_reviews")
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      def __repr__(self):
          return 'Review(desc=%s, rating=%s, reviewer=%s,book=%s created_at=%s,updated_at=%s )'% (self.desc, self.rating, self.reviewer, self.book, self.created_at, self.updated_at)
