from django.conf.urls import url
from . import views          
urlpatterns = [
	url(r'^$', views.index),     # Root route
    url(r'^process/register$', views.registerUser),
    url(r'^process/login$', views.loginUser),
    url(r'^books$', views.books),#success
    url(r'^process/logout$', views.logout),
	url(r'^books/add$', views.show_books_add),
	url(r'^books/(?P<id>[0-9]+)$', views.show_books),
	url(r'^process/add_book_add_review$', views.process_add_book_add_review),
	url(r'^process/add_review$', views.process_add_review),
	url(r'^users/(?P<id>[0-9]+)/$', views.show_user),
	url(r'^delete/(?P<id>[0-9]+)/$', views.destroy),
]
