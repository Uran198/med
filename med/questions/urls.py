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

    url(r'^delete/(?P<pk>[0-9]+)/$',
        views.QuestionDelete.as_view(),
        name='delete'
        ),

    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$',
        views.QuestionDetails.as_view(),
        name='details',
        ),

    url(r'^(?P<pk>[0-9]+)/$',
        views.QuestionDetails.as_view(),
        name='details',
        ),

    url(r'^$',
        views.QuestionList.as_view(),
        name='list',
        ),

    # Comments

    url(r'^comments/create/(?P<parent_id>[0-9]+)/$',
        views.CommentCreate.as_view(),
        name='add_comment',
        ),

    url(r'^comments/update/(?P<pk>[0-9]+)/$',
        views.CommentUpdate.as_view(),
        name='comment_update',
        ),

    url(r'^comments/delete /(?P<pk>[0-9]+)/$',
        views.CommentDelete.as_view(),
        name='comment_delete',
        ),
]
