from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$',
        views.CreateQuestion.as_view(),
        name='create',
        ),

    url(r'^update/(?P<pk>[0-9]+)/$',
        views.QuestionUpdate.as_view(),
        name='update'
        ),

    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$',
        views.QuestionDetails.as_view(),
        name='details',
        ),

    url(r'^(?P<pk>[0-9]+)/$',
        views.QuestionDetails.as_view(),
        name='details',
        ),
]
