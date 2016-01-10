# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns

from med.pages import views as pages_views

urlpatterns = [
    # Django set_language, user {% load i18n %}{% url 'set_language' %}
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^$', pages_views.HomeView.as_view(), name="home"),
    url(r'^about/$', pages_views.AboutView.as_view(), name="about"),
    url(r'^contact/$', pages_views.ContactView.as_view(), name="contact"),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("med.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^avatar/', include("avatar.urls")),

    # Search
    url(r'^search/', include('haystack.urls')),

    # Your stuff: custom urls with internationalization includes go here
    url(r'^questions/', include('med.questions.urls', namespace='questions')),
)

urlpatterns += [
    # Need no internationalization
    url(r'api/', include('med.api.urls', namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]
