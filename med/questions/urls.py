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

    url(r'^answers/create/(?P<parent_id>[0-9]+)/$',
        views.AnswerCreate.as_view(),
        name='add_answer',
        ),

    url(r'^answers/update/(?P<pk>[0-9]+)/$',
        views.AnswerUpdate.as_view(),
        name='answer_update',
        ),


    url(r'^answers/delete/(?P<pk>[0-9]+)/$',
        views.AnswerDelete.as_view(),
        name='answer_delete',
        ),


    # Comments

    url(r'^comments/questions/create/(?P<parent_id>[0-9]+)/$',
        views.QuestionCommentCreate.as_view(),
        name='add_comment',
        ),

    url(r'^comments/questions/update/(?P<pk>[0-9]+)/$',
        views.QuestionCommentUpdate.as_view(),
        name='comment_update',
        ),

    url(r'^comments/questions/delete/(?P<pk>[0-9]+)/$',
        views.QuestionCommentDelete.as_view(),
        name='comment_delete',
        ),

#    url(r'^comments/answers/create/(?P<parent_id>[0-9]+)/$',
#        views.AnswerCommentCreate.as_view(),
#        name='add_answer_comment',
#        ),
#
#    url(r'^comments/answers/update/(?P<pk>[0-9]+)/$',
#        views.AnswerCommentUpdate.as_view(),
#        name='answer_comment_update',
#        ),
#
#    url(r'^comments/answers/delete/(?P<pk>[0-9]+)/$',
#        views.AnswerCommentDelete.as_view(),
#        name='answer_comment_delete',
#        ),

    # Revisions

    url(r'^revisions/(?P<question_pk>[0-9]+)/$',
        views.RevisionList.as_view(),
        name='revision_list',
        ),
]
