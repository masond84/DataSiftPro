from django.urls import path
from . import views

app_name = 'helper'
urlpatterns = [
    path('', views.index, name="help_index"),
    path('newsletter-signup', views.newsletter, name="newsletter_signup"),
    #path('faqs/', views.faqs, name="faqs_page"),
]
