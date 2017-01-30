from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.index, name = "index"),
    url(r"^add_ticket/", views.add_ticket, name = "add_ticket"),
    url(r"^do_add_ticket/", views.do_add_ticket, name = "do_add_ticket"),
    url(r"^edit_user/", views.edit_user, name = "edit_user"),
    url(r"^do_edit_user/", views.do_edit_user, name = "do_edit_user"),
]
